"""AG-UI Weather Server Example.

This server hosts a weather-capable agent with access to:
- Weather MCP server (port 8001) for weather information
- User MCP server (port 8002) for user location data

The agent can answer weather queries for user-specified locations.
"""

import os

from agent_framework import ChatAgent, HostedMCPTool
from agent_framework.openai import OpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from fastapi import FastAPI
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI client
if os.environ.get("GITHUB_TOKEN") is not None:
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.github.ai/inference"
    model_name = os.environ.get("SMALL_DEPLOYMENT_MODEL_NAME")
    print("Using GitHub Token for authentication")
elif os.environ.get("AZURE_OPENAI_API_KEY") is not None:
    token = os.environ["AZURE_OPENAI_API_KEY"]
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    model_name = os.environ.get("SMALL_DEPLOYMENT_MODEL_NAME")
    print("Using Azure OpenAI Token for authentication")

async_openai_client = AsyncOpenAI(
    base_url=endpoint,
    api_key=token
)

openai_client = OpenAIChatClient(
    model_id=model_name,
    api_key=token,
    async_client=async_openai_client
)

# MCP server URLs
weather_mcp_url = os.getenv("WEATHER_MCP_URL", "http://localhost:8001/sse")
user_mcp_url = os.getenv("USER_MCP_URL", "http://localhost:8002/sse")

print(f"Weather MCP server: {weather_mcp_url}")
print(f"User MCP server: {user_mcp_url}")

# Create the weather-capable agent with MCP tools
agent = ChatAgent(
    name="WeatherAssistant",
    instructions=(
        "You are a helpful weather assistant with access to weather information and user location data. "
        "When users ask about weather, help them get accurate forecasts for their location. "
        "You can remember user locations across the conversation. "
        "If a user sets their location, remember it for future queries. "
        "Be friendly, concise, and informative in your responses."
    ),
    chat_client=openai_client,
    tools=[
        HostedMCPTool(
            name="Weather MCP",
            url=weather_mcp_url,
            approval_mode="never_require",
        ),
        HostedMCPTool(
            name="User MCP",
            url=user_mcp_url,
            approval_mode="never_require",
        ),
    ],
)

# Create FastAPI app
app = FastAPI(title="AG-UI Weather Server")

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    print("\nStarting AG-UI Weather Server on http://127.0.0.1:8888")
    print("Make sure MCP servers are running before connecting clients.\n")
    uvicorn.run(app, host="127.0.0.1", port=8888)
