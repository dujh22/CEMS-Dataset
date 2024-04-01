import json
import re
from detect_string_type import judge_language
import os

def is_pure_english(s):
    return judge_language(s) == 'en'


def has_chinese(s):
    return 'zh' in judge_language(s)  


def filter_data(input_file, output_dir):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    # 注意这一行_gpt需要后面修改掉！！！
    output_file = os.path.join(output_dir, base_name + '_calibration_gpt.jsonl')
    
    os.makedirs(output_dir, exist_ok=True)
    
    num = 0
    with open(input_file, 'r', encoding='utf-8') as fi, open(output_file, 'w', encoding='utf-8') as fo:
        for line in fi:
            data = json.loads(line)
            
            if "prompt" not in data or not is_pure_english(data["prompt"]):
                num += 1
                continue

            if "gpt_response" in data:
                response_field = "gpt_response"
            elif "glm_response" in data:
                response_field = "glm_response"
            else:
                num += 1
                continue

            if not is_pure_english(data[response_field]):
                num += 1
                continue
                
            if not has_chinese(data["response"]):
                num += 1
                continue  
                
            # 将ensure_ascii设为False来保持中文字符
            fo.write(json.dumps(data, ensure_ascii=False) + '\n')

    print("有问题的样例数: {}".format(num))

# 'output_directory' 是目标文件夹
filter_data('F:\code\github\ce\gpt_filter_saved_data_generate_concurrent\zh_en_mixed_0311_0327_5k.jsonl', 'F:\code\github\ce\glm_filter_saved_data_generate_concurrent_calibration')