from modelscope.hub.snapshot_download import snapshot_download

model_dir = snapshot_download('qwen/Qwen2-72B-Instruct-GPTQ-Int4')

# 在当前目录下创建一个名为model_dir的txt文件，里面包含model_dir变量的内容
with open('model_dir.txt', 'w') as f:
    f.write(model_dir)
