import json
import os
from difflib import SequenceMatcher

# 使用Python的difflib库，SequenceMatcher类可以比较两个字符串相似度。比较算法采用的是ratcliff/obershelp算法。
def calculate_overlap_ratio(str1, str2):
    return SequenceMatcher(None, str1, str2).ratio()

def calculate_chinese_ratio(str):
    cn_count = len([c for c in str if '\u4e00' <= c <= '\u9fa5'])
    total_count = len(str)
    if total_count == 0: return 0
    return cn_count / total_count

def calculate_ratio_for_json_lines(infile):
    overlap_ratios = []
    gpt3point5turbo_modify_response_chinese_ratios = []
    response_chinese_ratios = []
    prompt_chinese_ratios = []

    with open(infile, 'r', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            
            # Calculate overlap ratio
            overlap_ratios.append(
                calculate_overlap_ratio(
                    d["gpt3point5turbo_modify_response"], d["response"]))

            # Calculate chinese ratio for gpt3point5turbo_modify_response
            gpt3point5turbo_modify_response_chinese_ratios.append(
                calculate_chinese_ratio(d["gpt3point5turbo_modify_response"]))

            # Calculate chinese ratio for response
            response_chinese_ratios.append(
                calculate_chinese_ratio(d["response"]))

            # Calculate chinese ratio for prompt
            prompt_chinese_ratios.append(
                calculate_chinese_ratio(d["prompt"]))

    print("Overlap Ratio: Avg - {:.2%}, Max - {:.2%}, Min - {:.2%}".format(
        sum(overlap_ratios) / len(overlap_ratios),
        max(overlap_ratios),
        min(overlap_ratios)
    ))

    print("gpt3point5turbo_modify_response Chinese Ratio: Avg - {:.2%}, Max - {:.2%}, Min - {:.2%}".format(
        sum(gpt3point5turbo_modify_response_chinese_ratios) / len(gpt3point5turbo_modify_response_chinese_ratios),
        max(gpt3point5turbo_modify_response_chinese_ratios),
        min(gpt3point5turbo_modify_response_chinese_ratios)
    ))

    print("Response Chinese Ratio: Avg - {:.2%}, Max - {:.2%}, Min - {:.2%}".format(
        sum(response_chinese_ratios) / len(response_chinese_ratios),
        max(response_chinese_ratios),
        min(response_chinese_ratios)
    ))

    print("Prompt Chinese Ratio: Avg - {:.2%}, Max - {:.2%}, Min - {:.2%}".format(
        sum(prompt_chinese_ratios) / len(prompt_chinese_ratios),
        max(prompt_chinese_ratios),
        min(prompt_chinese_ratios)
    ))

# calculate_ratio_for_json_lines("F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice_removespace_noExam\\target_file_gpt3point5turbo22_removespace_noExam.jsonl")

if __name__ == '__main__':
    input_dir = "F://code//github//ce//data_has_batch_has_generate_has_modify_has_extract_choice"
    
    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_dir, file_name)

            # 调用处理函数
            print(f"正在处理文件：{input_file_path}")
            calculate_ratio_for_json_lines(input_file_path)
    
  