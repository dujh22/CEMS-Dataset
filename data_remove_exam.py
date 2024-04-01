import json
import re
import os

def check_exam_pattern(text):
    # 检查给定文本是否符合特定模式
    patterns = [r"\b[A-Z]\.", r"选项", r"options"]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def filter_jsonl(input_file_path):
    # 构建新文件名和新目录名
    dir_name, file_name = os.path.split(input_file_path)
    new_dir_name = f"{dir_name}_noExam"
    new_file_path = os.path.join(new_dir_name, f"{os.path.splitext(file_name)[0]}_noExam.jsonl")
    
    # 创建新目录（如果不存在）
    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)
    
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(new_file_path, 'w', encoding='utf-8') as output_file:
        for line in input_file:
            json_obj = json.loads(line)
            prompt = json_obj.get("prompt", "")
            response = json_obj.get("response", "")
            # 检查是否存在特定模式
            if not check_exam_pattern(prompt) and not check_exam_pattern(response):
                json.dump(json_obj, output_file, ensure_ascii=False)
                output_file.write("\n")  # 为了保持jsonl格式，每个JSON后添加换行符

# 用实际的文件路径替换以下路径
input_file_path = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice_removespace\\target_file_gpt3point5turbo22_removespace.jsonl"
filter_jsonl(input_file_path)
