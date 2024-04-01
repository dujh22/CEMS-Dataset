import json
from openai import OpenAI
from tqdm import tqdm
import os

# GLM API密钥和基本URL
api_key = "QGqhzEef29eGMA5buGB9JRrUdSweTCMe2Kcg4TGDdjGqwkJFLGW2h56Fccq86rYB"
base_url = "https://api.chatglm.cn/v1"

# 初始化GLM客户端
client = OpenAI(api_key=api_key, base_url=base_url)

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # 使用tqdm迭代器
        for line in tqdm(infile, desc='Processing'):
            # 解析每行JSON
            data = json.loads(line)
            history = data.get('history', [])
            prompt = data.get('prompt', '')

            # 构造messages
            messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": h['prompt'] if i % 2 == 0 else h['response']} for i, h in enumerate(history)]
            messages.append({"role": "user", "content": prompt})

            # 调用GLM接口
            stream = client.chat.completions.create(messages=messages, model="chatglm3-32b-v0.8-data", temperature=0.95, top_p=0.7, stream=True, max_tokens=1024)
            glm_response = ''.join(part.choices[0].delta.content or "" for part in stream)

            # 添加GLM响应到数据并保存
            data['glm_response'] = glm_response
            # json.dump(data, outfile)
            json.dump(data, outfile, ensure_ascii=False)
            #  确保了JSON输出保留了Unicode字符（比如中文），而不是将它们转换成了Unicode转义字符。这样一来，输出文件中的中文字符就会以正常的形式展现，而不是转义序列。
            outfile.write('\n')

out_dir = "F:\code\github\ce\glm_filter_saved_data_generate"
# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 调用函数处理文件
process_jsonl('F:\code\github\ce\glm_filter_saved_data\zh_en_mixed_0311_0327_5k.jsonl', 'F:\code\github\ce\glm_filter_saved_data_generate\zh_en_mixed_0311_0327_5k.jsonl')
