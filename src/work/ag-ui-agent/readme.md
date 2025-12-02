# AG-UI Weather Assistant Implementation

This implementation demonstrates Scenario 2: Building a user interface for your agent using the AG-UI protocol.

## Overview

The solution consists of three main components:

1. **MCP Servers** (Weather + User): Provide weather data and user information
2. **AG-UI Server**: Hosts the weather-capable agent with MCP tools
3. **AG-UI Client**: Console-based interface with location management

## Files Created

- `weather-ag-ui-server.py` - AG-UI server hosting the weather agent
- `weather-ag-ui-client.py` - Console client with location tracking
- `start-all-servers.sh` - Startup script for all services
- `stop-all-servers.sh` - Cleanup script to stop all services
- `start-mcp-servers.sh` - Script to start only MCP servers

## Architecture

```
┌─────────────────────┐
│  Console Client     │
│  (with location     │
│   management)       │
└──────────┬──────────┘
           │ AG-UI Protocol
           │ (HTTP/SSE)
           ▼
┌─────────────────────┐
│  AG-UI Server       │
│  (FastAPI)          │
└──────────┬──────────┘
           │
           ├─────────────┐
           ▼             ▼
    ┌─────────┐   ┌─────────┐
    │ Weather │   │  User   │
    │   MCP   │   │   MCP   │
    │ :8001   │   │ :8002   │
    └─────────┘   └─────────┘
```

## Quick Start

### 1. Start All Services

```bash
./start-all-servers.sh
```

This starts:
- Weather MCP server on port 8001
- User MCP server on port 8002
- AG-UI server on port 8888

### 2. Run the Client (in a new terminal)

```bash
cd /workspaces/frontier-agents-workshop/src/work
python weather-ag-ui-client.py
```

### 3. Stop All Services

```bash
./stop-all-servers.sh
```

## Usage Examples

The client supports these commands:

- `/location <city>` - Set your location
- `/help` - Show help
- `:q` or `quit` - Exit

### Test Queries

Try these example queries from the scenario:

1. **Set location and get weather:**
   ```
   Set my location to Seattle and tell me today's weather.
   ```

2. **Query with remembered location:**
   ```
   What will the weather be like tomorrow here?
   ```

3. **Conversation memory:**
   ```
   Can you summarize the last three things I asked you?
   ```

4. **Change location:**
   ```
   Change my location to Tokyo and give me a short forecast.
   ```

## Key Features

### Location Management

The client tracks user location in two ways:

1. **Explicit command**: `/location Seattle`
2. **Natural language**: "Set my location to Seattle"

Once set, the location is:
- Prepended to subsequent messages as context
- Remembered across the conversation
- Displayed in prompts

### AG-UI Protocol Benefits

- **Streaming responses**: Real-time agent output
- **Conversation threads**: Maintains context across queries
- **Activity tracking**: Visible tool calls and reasoning
- **Separation of concerns**: UI logic separate from agent logic

### MCP Tool Integration

The agent has access to:

- **Weather MCP**: Get forecasts for any location
- **User MCP**: Access user profile and preferences

These tools are invoked automatically by the agent when needed.

## Implementation Details

### Server (`weather-ag-ui-server.py`)

- Uses `ChatAgent` with `HostedMCPTool` for weather and user data
- Exposes AG-UI endpoint via FastAPI
- Runs on port 8888
- Agent instructions include location awareness

### Client (`weather-ag-ui-client.py`)

- Uses `AGUIChatClient` to connect to the server
- Maintains conversation thread for context
- Tracks user location locally
- Prepends location context to messages
- Streams agent responses with color formatting

### Startup Script (`start-all-servers.sh`)

- Starts services in correct order
- Waits between starts for initialization
- Logs output to `/tmp/*.log` files
- Saves PIDs for easy cleanup
- Shows status and instructions

## Troubleshooting

### Connection Issues

If the client can't connect to the server:

1. Verify all servers are running:
   ```bash
   ps aux | grep python
   ```

2. Check server logs:
   ```bash
   tail -f /tmp/weather-mcp.log
   tail -f /tmp/user-mcp.log
   tail -f /tmp/agui-server.log
   ```

3. Test MCP servers directly:
   ```bash
   curl http://localhost:8001/sse
   curl http://localhost:8002/sse
   ```

### Agent Not Using Tools

If the agent doesn't call weather tools:

- Check that MCP servers are running and accessible
- Verify the agent's instructions mention weather capabilities
- Try more explicit queries like "Get the weather for Seattle"

### Location Not Remembered

The client tracks location locally and prepends it to messages. Check:

- Location was set correctly (you should see "✓ Location set to: <city>")
- Subsequent messages include location context in square brackets

## Advanced Usage

### Custom Server URL

Set a different AG-UI server:

```bash
export AGUI_SERVER_URL="http://custom-host:9999/"
python weather-ag-ui-client.py
```

### Custom MCP Ports

Configure MCP server URLs:

```bash
export WEATHER_MCP_URL="http://localhost:9001/sse"
export USER_MCP_URL="http://localhost:9002/sse"
python weather-ag-ui-server.py
```

### Running Components Separately

Start only MCP servers:
```bash
./start-mcp-servers.sh
```

Start AG-UI server separately:
```bash
python weather-ag-ui-server.py
```

## Learning Points

1. **AG-UI Protocol**: Clean separation between UI and agent logic
2. **MCP Integration**: Agents can use multiple MCP servers as tools
3. **Location Context**: Client-side state can enhance agent capabilities
4. **Streaming**: Real-time response display improves user experience
5. **Thread Management**: Conversation continuity across multiple queries

## Next Steps

- Add more MCP tools (news, calendar, etc.)
- Implement multi-user support with authentication
- Add visual weather displays (ASCII art, charts)
- Build a web-based UI using the same AG-UI endpoint
- Add location validation and autocomplete
