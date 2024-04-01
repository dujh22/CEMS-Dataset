import json
import os

# 函数：递归地替换字符串中的连续空格
def replace_spaces(value):
    if isinstance(value, str):
        return ' '.join(value.split(' '))
    elif isinstance(value, list):
        return [replace_spaces(item) for item in value]
    elif isinstance(value, dict):
        return {key: replace_spaces(val) for key, val in value.items()}
    return value


# 函数：处理原始文件并生成新文件
def process_file(input_path, output_path):
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            # 递归处理每个键值对，替换字符串中的连续空格
            processed_data = replace_spaces(data)
            json.dump(processed_data, outfile, ensure_ascii=False)
            outfile.write('\n')


if __name__ == "__main__":
    # 定义输入和输出文件路径
    input_file_path = 'F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice\\target_file_gpt3point5turbo22.jsonl'
    output_file_path = 'F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify_choice_removespace\\target_file_gpt3point5turbo22_removespace.jsonl'

    # 调用函数处理文件
    process_file(input_file_path, output_file_path)




