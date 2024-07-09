from openai import OpenAI

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8008/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


# send a ChatCompletion request to count to 100
response = client.chat.completions.create(
    model="Qwen2-72B-Instruct-GPTQ-Int4",
    messages=[
        {"role": "system", "content": "你是一个有用的人工智能助手"},
        {"role": "user", "content": "为什么生鱼片其实是死鱼片？对此生成不少于1000字的解释。"},
    ],
    temperature=0,
    stream=True
)

# create variables to collect the stream of chunks
collected_messages = []
print("LLM: ", end="", flush=True)

# iterate through the stream of events
for chunk in response:
    chunk_message = chunk.choices[0].delta.content  # extract the message
    if not chunk_message:  # if the message is empty, skip it
        continue
    collected_messages.append(chunk_message)  # save the message
    print(chunk_message, end="", flush=True)  # print the response stream

