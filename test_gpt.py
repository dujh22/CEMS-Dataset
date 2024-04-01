# 适用版本 openai <= 0.28.1

import openai

openai.api_key = "sk-WKTbQOVHthXy0OOqAf5f95A70aB54dA18e062aD17a186619"
openai.api_base = "https://one-api.glm.ai/v1"

# create a chat completion
chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "你好"}])

# print the chat completion
print(chat_completion.choices[0].message.content)