#!/usr/bin/env bash

echo "Starting InstantStyle"
VENV_PATH=$(cat /workspace/InstantStyle/venv_path)
source ${VENV_PATH}/bin/activate
cd /workspace/InstantStyle
TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
export LD_PRELOAD="${TCMALLOC}"
export HF_HOME="/workspace"
nohup python3 gradio_demo/app.py --server_port 3001 > /workspace/logs/InstantStyle.log 2>&1 &
echo "InstantStyle started"
echo "Log file: /workspace/logs/InstantStyle.log"
deactivate
