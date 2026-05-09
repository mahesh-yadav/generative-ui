from copilotkit import CopilotKitMiddleware
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

import logging
logging.getLogger("langgraph.checkpoint.serde.jsonplus").setLevel(logging.ERROR)

agent = create_agent(
    model=ChatOpenAI(
        model="gpt-4.1-mini",
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

graph = agent
