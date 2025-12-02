#!/bin/bash

# Complete startup script for AG-UI Weather System
# Starts: MCP servers (weather + user) and AG-UI server

echo "=================================================="
echo "  Starting AG-UI Weather System"
echo "=================================================="
echo ""

# Start weather MCP server in the background
echo "1. Starting Weather MCP server on port 8001..."
cd ../../mcp-server/04-weather-server
nohup python run-mcp-weather.py > /tmp/weather-mcp.log 2>&1 &
WEATHER_PID=$!
sleep 2

# Start user MCP server in the background
echo "2. Starting User MCP server on port 8002..."
cd ../02-user-server
nohup python run-mcp-user.py > /tmp/user-mcp.log 2>&1 &
USER_PID=$!
sleep 2

# Return to ag-ui-agent directory and start AG-UI server
cd ../../work/ag-ui-agent
echo "3. Starting AG-UI Weather Server on port 8888..."
nohup python weather-ag-ui-server.py > /tmp/agui-server.log 2>&1 &
AGUI_PID=$!
sleep 2

echo ""
echo "=================================================="
echo "  All servers started successfully!"
echo "=================================================="
echo ""
echo "Running services:"
echo "  Weather MCP  (PID: $WEATHER_PID) → http://localhost:8001/sse"
echo "  User MCP     (PID: $USER_PID) → http://localhost:8002/sse"
echo "  AG-UI Server (PID: $AGUI_PID) → http://127.0.0.1:8888"
echo ""
echo "Server logs:"
echo "  Weather MCP:  /tmp/weather-mcp.log"
echo "  User MCP:     /tmp/user-mcp.log"
echo "  AG-UI Server: /tmp/agui-server.log"
echo ""
echo "To start the client in a new terminal, run:"
echo "  python weather-ag-ui-client.py"
echo ""
echo "To stop all servers, run:"
echo "  kill $WEATHER_PID $USER_PID $AGUI_PID"
echo ""
echo "Or press Ctrl+C and run:"
echo "  killall python"
echo ""
echo "=================================================="

# Save PIDs to file for easy cleanup
echo "$WEATHER_PID $USER_PID $AGUI_PID" > /tmp/agui-weather-pids.txt

# Wait for all processes
wait
