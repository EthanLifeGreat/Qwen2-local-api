# Qwen2-local-api
Qwen2 vllm OpenAI api &amp; gradio front-end

# Start
## 1. Install Dependencies
### conda env:

Install Anaconda dependencies listed in `environment.yml`, you may want to use command like this:

 `conda env create -f environment.yml -n qwen2`

### Auto-GPTQ:

```bash
unzip AutoGPTQ_v0.7.1.zip
cd AutoGPTQ_v0.7.1 && pip install -e .
```

### NCCL:
```bash
# Extract source code (you may want to download your own nccl files at nvidia.com)
tar -xvf nccl_2.22.3-1+cuda12.2_x86_64.txz
# Set NCCL path to the .so file
export VLLM_NCCL_SO_PATH=~/Qwen/nccl_2.22.3-1+cuda12.2_x86_64/lib/libnccl.so
```

Note that: this is for x86_64 machine and CUDA driver >= 12.0

You can download your version of NCCL Library at [NVIDIA Collective Communications Library (NCCL) | NVIDIA Developer](https://developer.nvidia.com/nccl/nccl-download)

## 2. Download Model
```bash
python model_download.py
```

## 3. Start Server

```bash
bash vllm_init.sh
```

Now an OpenAI API is supposed to be running on `http://0.0.0.0:8008`

## 4. Call API

for chatbot web demo, run

```bash
# start web UI on local IP port 8000 (by default)
python qw2_web_openai.py
```

for python API calling, run

```bash
# get whole response after processing
python openai_test.py
# get steaming resonse
python openai_test_streaming.py
```
