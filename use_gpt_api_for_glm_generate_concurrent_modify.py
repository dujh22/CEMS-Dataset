import json
import openai
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
from CalculationOfTheOverlapRate import calculate_chinese_ratio, calculate_overlap_ratio

# GPT API密钥和基本URL
api_key = "sk-WKTbQOVHthXy0OOqAf5f95A70aB54dA18e062aD17a186619"
base_url = "https://one-api.glm.ai/v1"



promt1 = "Given "
promt2 = "Please adjust the characters in this text according to the following requirements, with as few changes as possible, while maintaining the integrity of the message:\n\n1. Replace all Chinese characters with English characters.\n2. Remove all useless Chinese characters.\nThe return format is {\"response\":\"\"}."

# 设定API密钥和基本URL
openai.api_key = api_key
openai.api_base = base_url 

def process_line(line):
    # 尝试处理行，如果出现错误，则捕获异常并返回 None
    try:
        data = json.loads(line)
        if data.get('gpt3point5turbo_modify_response', '') != '':
            if calculate_chinese_ratio(data.get('gpt3point5turbo_modify_response', '')) == 0:
                if calculate_overlap_ratio(data.get('gpt3point5turbo_modify_response', ''), data.get('response', '')) > 0.9:
                    return data
        
        for i in range(50):
            response = data.get('response', '')
            last_prompt = promt1 + json.dumps({"response":response}, ensure_ascii=False) + promt2

            messages = [{"role": "user", "content": last_prompt}]
            
            # 添加用户输入的提示和响应
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
            gpt_response = chat_completion.choices[0].message.content

            try:
                new_response = json.loads(gpt_response)
            except:
                new_response = {"response": ''}
            data['gpt3point5turbo_modify_response'] = new_response.get('response', '')
            # 检查是否需要继续调用API
            if calculate_chinese_ratio(data.get('gpt3point5turbo_modify_response', '')) == 0:
                if calculate_overlap_ratio(data.get('gpt3point5turbo_modify_response', ''), data.get('response', '')) > 0.9:
                    break

    except Exception as ex:
        print(f'An error occurred: {ex}')
        data = None   # 当发生错误时，返回 None
    
    return data

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = list(tqdm(infile, desc='Processing'))

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(tqdm(executor.map(process_line, lines), total=len(lines)))

        for data in results:
            if data is not None:  # 只有当 data 不为 None 时才写入文件
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')

out_dir = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

input_file = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify\\target_file_gpt3point5turbo20.jsonl"
output_file = os.path.join(out_dir, "target_file_gpt3point5turbo21.jsonl")
process_jsonl(input_file, output_file)

# 检测有多少个data拥有了gpt3point5turbo_modify_response属性
count = 0
sum = 0
with open(output_file, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('gpt3point5turbo_modify_response', '') != '':
            count += 1
        sum += 1
print(f"有{count}个data拥有了gpt3point5turbo_modify_response属性")
print(f"共计有{sum}个data")

