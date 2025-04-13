#!/bin/bash

#SBATCH --job-name=training_data_thoughts
#SBATCH --partition=debug
#SBATCH --output=logs/training_data_thoughts.out
#SBATCH --error=logs/training_data_thoughts.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:A6000:1
#SBATCH --mem=100G


#vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-14B --port 8000 --dtype=float32 --max_model_len 100000 --tensor-parallel-size 4 --enable-reasoning --reasoning-parser deepseek_r1 &
vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-14B --port 8000 --max_model_len 50000 --enable-reasoning --reasoning-parser deepseek_r1 &

echo "Waiting for vLLM server to start..."
until curl -s http://localhost:8000/ping > /dev/null; do
   sleep 5
done

echo "vLLM server is up and running."

source venv/bin/activate
python3 eval.py
