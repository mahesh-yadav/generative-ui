from __future__ import annotations

import threading
import warnings

warnings.filterwarnings("ignore")

import uvicorn
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import CopilotKitMiddleware, LangGraphAGUIAgent
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

import logging
logging.getLogger("langgraph.checkpoint.serde.jsonplus").setLevel(logging.ERROR)


_SERVER_STARTED = False
_SERVER_LOCK = threading.Lock()


def _kill_port(port: int) -> None:
    """Kill any process currently listening on *port*."""
    import os, subprocess as _sp, time
    try:
        result = _sp.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True)
        for pid in result.stdout.strip().split():
            if pid:
                print(f"⚠ Found existing process (PID {pid}) on port {port} — killing it")
                os.kill(int(pid), 9)
        if result.stdout.strip():
            time.sleep(0.5)
    except Exception:
        pass


def _build_graph():
    return create_agent(
        model=ChatOpenAI(
            model="gpt-4.1",
        ),
        tools=[],
        middleware=[CopilotKitMiddleware()],
        checkpointer=MemorySaver(),
        system_prompt=(
            "You are a helpful assistant. "
            "When users ask for whiteboards, design tools, or planning spaces, "
            "use available MCP app tools."
        ),
    )


def start_backend(
    host: str = "0.0.0.0",
    port: int = 8000,
    log_level: str = "warning",
) -> dict[str, str]:
    global _SERVER_STARTED

    app = FastAPI()
    agent = LangGraphAGUIAgent(
        name="app_agent",
        description="Simple MCP app agent",
        graph=_build_graph(),
    )
    add_langgraph_fastapi_endpoint(app=app, agent=agent, path="/")

    with _SERVER_LOCK:
        if not _SERVER_STARTED:
            _kill_port(port)
            threading.Thread(
                target=lambda: uvicorn.run(app, host=host, port=port, log_level=log_level),
                daemon=True,
            ).start()
            _SERVER_STARTED = True

    return {"url": f"http://localhost:{port}"}
