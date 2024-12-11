#!/usr/bin/env bash

# Function to stop both servers
stop_servers() {
    echo "Stopping uvicorn server..."
    kill "$uvicorn_pid" 2>/dev/null
    echo "Stopping Vue.js server..."
    kill "$vue_server_pid" 2>/dev/null
}

# Set up a trap to stop both servers when the script is terminated
trap stop_servers SIGINT SIGTERM

echo "Starting database server..."
sudo systemctl start mariadb

# Start the uvicorn server in the background
echo "Starting uvicorn server..."
uvicorn main:app --host 127.0.0.1 --port 8000 &
uvicorn_pid=$!

# Navigate to the frontend directory and start the Vue.js server in the background
echo "Starting Vue.js server..."
cd app/frontend/tm_frontend || exit
npm run serve &
vue_server_pid=$!
cd ../../..

# Wait for both servers to finish (or keep the script running)
wait "$uvicorn_pid"
wait "$vue_server_pid"
