import json
import re
import os
from tqdm import tqdm
from CalculationOfTheOverlapRate import calculate_chinese_ratio, calculate_overlap_ratio

def has_chinese_char(string):
    """Helper function to check if a string includes Chinese characters."""
    return bool(re.search('[\u4e00-\u9fa5]', string))

def process_file(input_file, output_file=""):
    """Process JSONL file."""
    # Open input file and output (new) file
    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out: 
        # Process each line (JSON object)
        for line in tqdm(f_in, desc='Processing'):
            data = json.loads(line.strip())
            # Remove 'gpt_response' and 'glm_response'
            data.pop('gpt_response', None)
            data.pop('glm_response', None)
            data.pop('raw_response', None)
            # Remove Chinese char from 'history'
            data['history'] = [] if any(has_chinese_char(str(item)) for item in data['history']) else data['history']
            # Write to file
            if data.get('gpt3point5turbo_modify_response', '') != '':
                if calculate_overlap_ratio(data.get('gpt3point5turbo_modify_response', ''), data.get('response', '')) > 0.9:
                    if calculate_chinese_ratio(data['gpt3point5turbo_modify_response']) == 0:
                        f_out.write(json.dumps(data, ensure_ascii=False) + "\n")

# 实例：调用函数处理文件
# input_dir = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify"
# file_name = 'target_file_gpt3point5turbo22.jsonl'
# input_file = os.path.join(input_dir, file_name)
# out_dir = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice"
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)
# output_file = os.path.join(out_dir, file_name)

# # Call the function. Replace 'source.jsonl' with your source file name and 'target.jsonl' with your target filename.
# process_file(input_file, output_file)

def main():
    input_dir = "F://code//github//ce//data_has_batch_has_generate_has_extract_has_modify_merge"
    output_dir = "F://code//github//ce//data_has_batch_has_generate_has_extract_has_modify_merge_choice"

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            # # 如果输出文件已存在，则跳过处理
            # if os.path.exists(output_file_path):
            #     print(f"{file_name} 已存在，跳过处理。")
            #     continue

            # 调用处理函数
            print(f"正在处理文件：{input_file_path}")
            process_file(input_file_path, output_file_path)
            print(f"处理完成，输出文件：{output_file_path}")

if __name__ == "__main__":
    main()
