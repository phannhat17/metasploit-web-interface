#!/bin/bash

# Switching to virtual environment
echo -e "\e[35m[*] Switching to venv\e[0m"
source .venv/bin/activate

# Generating msfRPC server password
echo -e "\e[32m[*] Generating msfRPC server password\e[0m"
export MSFPASS=$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 20)
echo $MSFPASS

# Starting msfRPC server in the background
echo -e "\e[34m[*] Starting MSGRPC server\e[0m"
msfrpcd -P "$MSFPASS" &

# Wait for msfrpcd to be ready (listening on port 55553)
echo "Waiting for msfRPC server to start..."
while ! nc -z localhost 55553; do   
  sleep 1 # Wait for 1 second before check again
done
echo "msfRPC server is up and running."

# Starting Flask app
echo -e "\e[36m[*] Starting flask app\e[0m"
python app.py

