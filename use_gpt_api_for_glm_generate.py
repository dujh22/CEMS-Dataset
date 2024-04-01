# 适用版本 openai <= 0.28.1

import json
import openai
from tqdm import tqdm
import os
import config

# GPT API密钥和基本URL
api_key = config.GPT_API_KEY
base_url = config.GPT_BASE_URL

# 设定API密钥和基本URL
openai.api_key = api_key
openai.api_base = base_url

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # 使用tqdm迭代器
        i = 0
        for line in tqdm(infile, desc='Processing'):
            i += 1
            if i == 5:
                break
            # 解析每行JSON
            data = json.loads(line)
            history = data.get('history', [])
            prompt = data.get('prompt', '')

            # 构造messages
            messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": h['prompt'] if i % 2 == 0 else h['response']} for i, h in enumerate(history)]
            messages.append({"role": "user", "content": prompt})

            # 调用GPT接口
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
            gpt_response = chat_completion.choices[0].message.content

            # 添加GPT响应到数据并保存
            data['gpt_response'] = gpt_response
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write('\n')

out_dir = "F:\code\github\ce\glm_filter_saved_data_generate_gpt"
# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 调用函数处理文件
process_jsonl('F:\code\github\ce\glm_filter_saved_data\zh_en_mixed_0311_0327_5k.jsonl', 'F:\code\github\ce\glm_filter_saved_data_generate_gpt\zh_en_mixed_0311_0327_5k.jsonl')