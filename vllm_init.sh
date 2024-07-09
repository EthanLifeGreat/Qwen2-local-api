#!/usr/bin/bash -x
# Set model path to the path in model_dir.txt
export MODEL_PATH=$HOME/.cache/modelscope/hub/qwen/Qwen2-72B-Instruct-GPTQ-Int4
echo "MODEL_PATH: $MODEL_PATH"
echo "which python: $(which python)"
# Start the API server
python -m vllm.entrypoints.openai.api_server --model "$MODEL_PATH" --served-model-name Qwen2-72B-Instruct-GPTQ-Int4 --tensor-parallel-size 4 --host 0.0.0.0 --port 8008
