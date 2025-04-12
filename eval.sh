#!/bin/bash

vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B --port 8000 --dtype=float32 --max_model_len 100000 --enable-reasoning --reasoning-parser deepseek_r1 &
echo "Waiting for vLLM server to start..."
until curl -s http://localhost:8000/ping > /dev/null; do
   sleep 5
done

echo "vLLM server is up and running."

python3 eval.py
