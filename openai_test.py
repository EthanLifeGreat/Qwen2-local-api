from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8008/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

chat_response = client.chat.completions.create(
    model="Qwen2-72B-Instruct-GPTQ-Int4",
    messages=[
        {"role": "system", "content": "你是一个有用的人工智能助手"},
        {"role": "user", "content": "为什么生鱼片其实是死鱼片？对此生成不少于1000字的解释。"},
    ]
)
print("Chat response:", chat_response)
