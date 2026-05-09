from __future__ import annotations

import os
import warnings

warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

HOST = "0.0.0.0"
PORT = 8001
GEMINI_MODEL = "gemini-flash-latest"
OPENAI_MODEL = "gpt-5.4-mini-2026-03-17"

app = FastAPI()
gemini_agent = Agent(
    name="basic_adk_agent",
    model=LiteLlm(model_name=OPENAI_MODEL),
    instruction="You are a helpful assistant"
)
adk_agent = ADKAgent(
    adk_agent=gemini_agent,
    app_name="demo_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)
add_adk_fastapi_endpoint(app=app, agent=adk_agent, path="/")

def main() -> None:
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")


if __name__ == "__main__":
    main()