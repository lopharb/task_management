#!/usr/bin/env fish

# Function to stop both servers
function stop_servers
    echo "Stopping uvicorn server..."
    kill $uvicorn_pid
    echo "Stopping Vue.js server..."
    kill $http_server_pid
end

# Set up a trap to stop both servers when the script is terminated
trap stop_servers SIGINT SIGTERM

echo "Starting database server..."
sudo systemctl start mariadb
# Start the uvicorn server in the background
echo "Starting uvicorn server..."
uvicorn main:app --host 127.0.0.1 --port 8000 &
set uvicorn_pid $last_pid

# Navigate to the frontend directory and start the Python HTTP server in the background
echo "Starting Vue.js server..."
cd app/frontend/tm_frontend
npm run serve
set http_server_pid $last_pid
cd ../../..

# Wait for both servers to finish (or keep the script running)
wait $uvicorn_pid
wait $http_server_pid
