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

last_prompt = "Please further check if the previous response is correct: \n If it is correct, return {\"response\": \"yes\"} \n If it is incorrect, return the correct response in {\"response\":\"\"}"

def process_line(line):
    # 尝试处理行，如果出现错误，则捕获异常并返回 None
    try:
        data = json.loads(line)
        data["is_correct"] = "no"
        data["version"] = 1
        prompt = data.get('prompt', '')

        for i in range(5):
            gpt_response = data.get('gpt3point5turbo_modify_response', '')

            history = data.get('history', [])
            # 构造messages
            messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": h['prompt'] if i % 2 == 0 else h['response']} for i, h in enumerate(history)]
            
            temp_messages = {"role": "user", "content": prompt}
            messages.append(temp_messages)
            temp_messages2 = {"role": "assistant", "content": gpt_response}
            messages.append(temp_messages2)
            temp_messages3 = {"role": "user", "content": last_prompt}
            messages.append(temp_messages3)
            
            # 添加用户输入的提示和响应
            chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages)
            gpt_response = chat_completion.choices[0].message.content

            try:
                new_response = json.loads(gpt_response)
            except:
                new_response = {"response": ''}

            if new_response.get('response', '') == 'yes':
                data["is_correct"] = "yes"
                break
            else:
                data['gpt3point5turbo_modify_response'] = new_response.get('response', '')
                data['version'] += 1

    except Exception as ex:
        print(f'An error occurred: {ex}')
        data = None   # 当发生错误时，返回 None
    
    return data

def process_jsonl(input_file, output_file1, output_file2):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file1, 'w', encoding='utf-8') as outfile1, open(output_file2, 'w', encoding='utf-8') as outfile2:
        lines = list(tqdm(infile, desc='Processing'))

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(tqdm(executor.map(process_line, lines), total=len(lines)))

        for data in results:
            if data is not None:  # 只有当 data 不为 None 时才写入文件
                # json.dump(data, outfile, ensure_ascii=False)
                if data['version'] == 1:
                    outfile1.write(json.dumps(data, ensure_ascii=False) + '\n')
                else:
                    outfile2.write(json.dumps(data, ensure_ascii=False) + '\n')   

out_dir = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice_removespace_splitForCorrect"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

input_file = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice_removespace\\target_file_gpt3point5turbo20.jsonl"
output_file1 = os.path.join(out_dir, "target_file_gpt3point5turbo21_correct.jsonl")
output_file2 = os.path.join(out_dir, "target_file_gpt3point5turbo22_modigy_need_check.jsonl")
process_jsonl(input_file, output_file1, output_file2)



