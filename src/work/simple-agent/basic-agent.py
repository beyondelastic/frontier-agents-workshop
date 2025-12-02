import os
import asyncio

from agent_framework import ChatAgent, HostedMCPTool
from agent_framework.openai import OpenAIChatClient

from openai import AsyncOpenAI

from dotenv import load_dotenv

load_dotenv()

"""
Agent with Local MCP Servers Example

Demonstrates connecting an agent to local MCP servers (weather and user)
running on localhost ports 8001 and 8002.
"""


if (os.environ.get("GITHUB_TOKEN") is not None):
    token = os.environ["GITHUB_TOKEN"]
    endpoint = "https://models.github.ai/inference"
    print("Using GitHub Token for authentication")
elif (os.environ.get("AZURE_OPENAI_API_KEY") is not None):
    token = os.environ["AZURE_OPENAI_API_KEY"]
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    print("Using Azure OpenAI Token for authentication")

async_openai_client = AsyncOpenAI(
    base_url=endpoint,
    api_key=token
)

completion_model_name = os.environ.get("COMPLETION_DEPLOYMENT_NAME")
medium_model_name = os.environ.get("MEDIUM_DEPLOYMENT_MODEL_NAME")
small_model_name = os.environ.get("SMALL_DEPLOYMENT_MODEL_NAME")

completion_client=OpenAIChatClient(
    model_id = completion_model_name,
    api_key=token,
    async_client = async_openai_client
)

medium_client=OpenAIChatClient(
    model_id = medium_model_name,
    api_key=token,
    async_client = async_openai_client
)

small_client=OpenAIChatClient(
    model_id = small_model_name,
    api_key=token,
    async_client = async_openai_client
)


async def main() -> None:
    # MCP server URLs
    weather_mcp_url = os.getenv("WEATHER_MCP_URL", "http://localhost:8001/sse")
    user_mcp_url = os.getenv("USER_MCP_URL", "http://localhost:8002/sse")
    
    print(f"Connecting to Weather MCP server at: {weather_mcp_url}")
    print(f"Connecting to User MCP server at: {user_mcp_url}")
    
    # Create agent with both MCP servers as tools
    async with ChatAgent(
        chat_client=small_client,
        name="MultiMCPAgent",
        instructions=(
            "You are a helpful assistant with access to weather and user information tools. "
            "Use the weather MCP server to get weather information and the user MCP server "
            "to get user-related information. Be concise and helpful in your responses."
        ),
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
    ) as agent:
        # Example query that can use both MCP servers
        message = "What's the weather in Amsterdam and in Paris?"
        print(f"\nUser: {message}")
        
        result = await agent.run(message)
        print(f"Assistant: {result}")


if __name__ == "__main__":
    asyncio.run(main())