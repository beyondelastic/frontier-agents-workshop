"""AG-UI Weather Client with Location Management.

This client connects to the AG-UI weather server and allows users to:
- Set their location for weather queries
- Ask weather-related questions
- Maintain conversation context across queries

Commands:
- /location <city>  - Set your location
- /help            - Show help
- :q or quit       - Exit
"""

import asyncio
import os

from agent_framework import ChatAgent
from agent_framework_ag_ui import AGUIChatClient
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:
    """Weather client with location management."""

    def __init__(self, server_url: str):
        """Initialize the weather client."""
        self.server_url = server_url
        self.user_location = None
        self.chat_client = AGUIChatClient(endpoint=server_url)
        self.agent = ChatAgent(
            name="WeatherClientAgent",
            chat_client=self.chat_client,
            instructions="You are a helpful assistant that helps users with weather information.",
        )
        self.thread = self.agent.get_new_thread()

    def show_help(self):
        """Display help information."""
        print("\n" + "="*60)
        print("Weather Assistant - Commands:")
        print("="*60)
        print("/location <city>  - Set your location for weather queries")
        print("/help            - Show this help message")
        print(":q or quit       - Exit the application")
        print("\nExample queries:")
        print('  "Set my location to Seattle and tell me today\'s weather."')
        print('  "What will the weather be like tomorrow here?"')
        print('  "Change my location to Tokyo and give me a short forecast."')
        print("="*60 + "\n")

    def set_location(self, location: str):
        """Set the user's location."""
        self.user_location = location
        print(f"\n✓ Location set to: {location}\n")

    def get_location_context(self) -> str:
        """Get location context to prepend to user messages."""
        if self.user_location:
            return f"[User's current location: {self.user_location}] "
        return ""

    async def process_message(self, message: str) -> bool:
        """Process a user message. Returns False if should exit."""
        message = message.strip()

        # Handle empty input
        if not message:
            print("Request cannot be empty.")
            return True

        # Handle exit commands
        if message.lower() in (":q", "quit"):
            return False

        # Handle help command
        if message.lower() == "/help":
            self.show_help()
            return True

        # Handle location command
        if message.lower().startswith("/location "):
            location = message[10:].strip()
            if location:
                self.set_location(location)
            else:
                print("Usage: /location <city>")
            return True

        # Check if message contains location setting instruction
        if "set my location" in message.lower() or "change my location" in message.lower():
            # Let the agent handle it but also track it locally
            import re
            location_match = re.search(r'(?:set|change) (?:my )?location to ([A-Za-z\s]+)', message, re.IGNORECASE)
            if location_match:
                location = location_match.group(1).strip()
                # Extract just the city name (before "and" if present)
                if " and " in location:
                    location = location.split(" and ")[0].strip()
                self.user_location = location

        # Add location context to message if location is set
        full_message = self.get_location_context() + message

        # Stream the agent response
        print("\nAssistant: ", end="", flush=True)
        try:
            async for update in self.agent.run_stream(full_message, thread=self.thread):
                # Print text content as it streams
                if update.text:
                    print(f"\033[96m{update.text}\033[0m", end="", flush=True)
            print("\n")
        except Exception as e:
            print(f"\n\033[91mError communicating with server: {e}\033[0m")
            print("Make sure the AG-UI server and MCP servers are running.\n")

        return True

    async def run(self):
        """Run the main client loop."""
        print(f"Connecting to AG-UI server at: {self.server_url}\n")
        self.show_help()

        try:
            while True:
                # Get user input
                message = input("User (:q to exit, /help for commands): ")

                # Process the message
                should_continue = await self.process_message(message)
                if not should_continue:
                    break

        except KeyboardInterrupt:
            print("\n\nExiting...")
        except Exception as e:
            print(f"\n\033[91mAn error occurred: {e}\033[0m")


async def main():
    """Main entry point."""
    # Get server URL from environment or use default
    server_url = os.environ.get("AGUI_SERVER_URL", "http://127.0.0.1:8888/")

    # Create and run the client
    client = WeatherClient(server_url)
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())
