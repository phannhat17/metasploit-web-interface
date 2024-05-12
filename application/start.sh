#!/bin/bash

sudo msfdb init

echo -e "\e[35m[*] Switching to venv\e[0m"
source .venv/bin/activate

export PYTHONDONTWRITEBYTECODE=1 

# Check if msfRPC server is already running
echo -e "\e[31m[*] Checking if msfRPC server is running..."
if nc -z localhost 55553; then
    echo -e "\e[31m[i] msf RPC server is already running. Killing the existing process.\e[0m"
    # Kill the existing msfRPC server process
    MSFRPC_PID=$(lsof -ti:55553)
    if [ ! -z "$MSFRPC_PID" ]; then
        sudo kill -9 $MSFRPC_PID
        echo -e "\e[31m[i] Killed the existing msfRPC server process.\e[0m"
    fi
fi

# Check and set MSFPASS
if [ -z "${MSFPASS}" ]; then
    echo -e "\e[32m[*] Generating msfRPC server password\e[0m"
    export MSFPASS=$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 20)
    echo "    Generated msfRPC server password: $MSFPASS"
fi

# Starting msfRPC server in the background
echo -e "\e[34m[*] Starting msfRPC server\e[0m"
msfrpcd -P "$MSFPASS" &&

echo -e "\e[34m[i] Waiting for msfRPC server to start..."
while ! nc -z localhost 55553; do   
    sleep 1
done
echo -e "\e[34m[i] msfRPC server is up and running."

# Starting Flask app
echo -e "\e[36m[*] Starting Flask app\e[0m"
python app.py &