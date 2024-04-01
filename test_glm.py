# 适用版本 openai == 1.14.3
from openai import OpenAI

client = OpenAI(api_key="QGqhzEef29eGMA5buGB9JRrUdSweTCMe2Kcg4TGDdjGqwkJFLGW2h56Fccq86rYB",
                base_url="https://api.chatglm.cn/v1")

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "你好！请问你是？",
        }
    ],
    model="chatglm3-32b-v0.8-data",
    temperature=0.95,
    top_p=0.7,
    stream=True,
    max_tokens=1024
)

for part in stream:
    print(part.choices[0].delta.content or "", end="", flush=True)

print()