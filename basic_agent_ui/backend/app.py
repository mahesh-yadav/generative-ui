from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from langgraph.checkpoint.memory import MemorySaver
from copilotkit import LangGraphAGUIAgent, CopilotKitMiddleware

HOST = "0.0.0.0"
PORT = 8000
OPENAI_MODEL = "gpt-5.4-mini-2026-03-17"
GEMINI_MODEL = "gemini-flash-latest"

app = FastAPI()
graph = create_agent(
    model=ChatOpenAI(model=OPENAI_MODEL),
    tools=[],
    middleware=[CopilotKitMiddleware()],
    checkpointer=MemorySaver(),
    system_prompt=(
        "You are a helpful assistant."
    )
)
agent = LangGraphAGUIAgent(
    name="basic-agent",
    description="basic agent for demonstration",
    graph=graph,
)
add_langgraph_fastapi_endpoint(app=app, agent=agent, path="/")

def main() -> None:
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()