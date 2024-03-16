#!/bin/bash
echo -e "\e[32m[*] Generating msfRPC server password\e[0m" && export MSFPASS=$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 20) && echo $MSFPASS && echo -e "\e[34m[*] Starting MSGRPC server\e[0m" && msfrpcd -P "$MSFPASS"
echo -e "\e[35m[*] Switching to venv\e[0m"
source .venv/bin/activate && echo -e "\e[36m[*] Starting flask app\e[0m" && python app.py