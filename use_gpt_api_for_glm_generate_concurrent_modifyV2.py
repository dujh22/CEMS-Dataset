import json
import openai
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
from CalculationOfTheOverlapRate import calculate_chinese_ratio, calculate_overlap_ratio
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
        data['gpt3point5turbo_modify_response'] = ''
        
        # 检查问题
        for i in range(5):
            question = data.get('prompt', '')
            messages = [{"role": "user", "content": "Given {\"question\":{" + question + "}}, determine if that\n\n 1. it is a translation task, e.g. to translate into a certain language\n 2. it is an English question parsing task, e.g., an English multiple-choice question.\n 3. it's a code task, e.g., you want to use some programming language to complete the specified task.\n If it is any of the above cases, the return format is {\"answer\": \"yes\"}.\n If it is not one of the above cases, the return format is {\"answer\": \"no\"}."}]
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
            gpt_response = chat_completion.choices[0].message.content
            try:
                new_response = json.loads(gpt_response)
            except:
                new_response = {"answer": ''}
            
            if new_response.get('answer', '') == 'yes':
                data = None
                return data
            elif new_response.get('answer', '') == 'no':
                break

        # 生成答案               
        for j in range(5):
            response = data.get('response', '')
            messages2 = [{"role": "user", "content": "Given {\"response\":" + response + "}. \n Please adjust the characters in the text according to the following requirements while maintaining the integrity of the information: \n\n 1. first see if the Chinese characters are redundant, if they are redundant or useless, eliminate them. \n 2. express all Chinese characters that need to be retained but have not been translated into English as English, paying attention to the lexical properties and whether the translation is smooth. \n 3. Reasonably adjust the order and layout of statements according to the context to ensure that the optimized reply is fluent and free of speech defects. \n Note: \n 1. formatting information should be retained \n 2. change as little as possible \n The return format is {\"response\":\"\"}."}]
            # 添加用户输入的提示和响应
            chat_completion2 = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages2)
            gpt_response2 = chat_completion2.choices[0].message.content
            try:
                new_response2 = json.loads(gpt_response2)
            except:
                new_response2 = {"response": ''}
            data['gpt3point5turbo_modify_response'] = new_response2.get('response', '')
            if data['gpt3point5turbo_modify_response'] != '':
                break
             
        # 检查答案
        for k in range(5):
            response = data.get('response', '')
            gpt_response = data.get('gpt3point5turbo_modify_response', '')
            messages3 = [{"role": "user", "content": "Given {\"prompt\":" + response + ", \"response\":" + gpt_response + "}. \n On the premise of keeping the information complete, please check whether the response is adjusted for the characters in the prompt according to the following requirements: \n 1. first see whether the Chinese characters are redundant or not, if redundant or useless, eliminate them.\n 2. all Chinese characters that need to be retained but not translated into English should be expressed in English, paying attention to the lexical nature and whether the translated statement is fluent or not \n 3. Reasonably adjust the order and layout of statements according to the context to ensure that the optimized reply is fluent and free of speech defects.\n 4. Formatting information should be retained and changed as little as possible.\n If the response has been adjusted as described above, return {\"response\": \"yes\"}\n If the response is not adjusted according to the above requirements, please re-adjust the gpt_response according to the above requirements, and return {\"response\":\"\"}."}]
            # 添加用户输入的提示和响应
            chat_completion3 = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages3)
            gpt_response3 = chat_completion3.choices[0].message.content
            try:
                new_response3 = json.loads(gpt_response3)
            except:
                new_response3 = {"response": ''}
            temp_response = new_response3.get('response', '')
            if temp_response == "yes":
                break
            elif temp_response != "":
                data['gpt3point5turbo_modify_response'] = temp_response
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

input_file = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify\\target_file_gpt3point5turboA1 copy.jsonl"
output_file = os.path.join(out_dir, "target_file_gpt3point5turboA1 copy_test.jsonl")
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

