import json
import openai
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
import config

# GPT API密钥和基本URL
api_key = config.GPT_API_KEY
base_url = config.GPT_BASE_URL

# 设定API密钥和基本URL
openai.api_key = api_key
openai.api_base = base_url 

def process_line(line):
    # 尝试处理行，如果出现错误，则捕获异常并返回 None
    try:
        data = json.loads(line)
        history = data.get('history', [])
        prompt = data.get('prompt', '')

        messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": h['prompt'] if i % 2 == 0 else h['response']} for i, h in enumerate(history)]
        messages.append({"role": "user", "content": prompt})

        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
        gpt_response = chat_completion.choices[0].message.content

        data['gpt_response'] = gpt_response

    except Exception as ex:
        print(f'An error occurred: {ex}')
        data = None   # 当发生错误时，返回 None
    
    return data

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = list(tqdm(infile, desc='Processing'))

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(tqdm(executor.map(process_line, lines), total=len(lines)))

        for data in results:
            if data is not None:  # 只有当 data 不为 None 时才写入文件
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')

out_dir = "F:\code\github\ce\gpt_filter_saved_data_generate_concurrent"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

process_jsonl('F:\code\github\ce\glm_filter_saved_data\zh_en_mixed_0311_0327_5k.jsonl', 'F:\code\github\ce\gpt_filter_saved_data_generate_concurrent\zh_en_mixed_0311_0327_5k.jsonl')