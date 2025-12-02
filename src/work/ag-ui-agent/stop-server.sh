#!/bin/bash

# Stop all AG-UI Weather System servers

echo "Stopping AG-UI Weather System servers..."

# Try to stop using saved PIDs
if [ -f /tmp/agui-weather-pids.txt ]; then
    PIDS=$(cat /tmp/agui-weather-pids.txt)
    echo "Stopping servers (PIDs: $PIDS)..."
    kill $PIDS 2>/dev/null
    rm /tmp/agui-weather-pids.txt
fi

# Fallback: kill all python processes running the servers
pkill -f "run-mcp-weather.py"
pkill -f "run-mcp-user.py"
pkill -f "weather-ag-ui-server.py"

echo "All servers stopped."
