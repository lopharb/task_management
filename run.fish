#!/usr/bin/env fish

# Function to stop both servers
function stop_servers
    echo "Stopping uvicorn server..."
    kill $uvicorn_pid
    echo "Stopping Python HTTP server..."
    kill $http_server_pid
end

# Set up a trap to stop both servers when the script is terminated
trap stop_servers SIGINT SIGTERM

# Start the uvicorn server in the background
echo "Starting uvicorn server..."
uvicorn main:app --host 127.0.0.1 --port 8000 &
set uvicorn_pid $last_pid

# Navigate to the frontend directory and start the Python HTTP server in the background
echo "Starting Python HTTP server in frontend directory..."
cd app/frontend
python3 -m http.server 3000 &
set http_server_pid $last_pid

# Wait for both servers to finish (or keep the script running)
wait $uvicorn_pid
wait $http_server_pid

cd ../..