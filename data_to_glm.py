import json
import os
import glob
import uuid
from tqdm import tqdm

def format_single_dict(single_dict):
    """
    将单个字典从现有格式转换为新格式
    """
    return {
        "prompt": single_dict["question"],
        "response": single_dict["response_chosen"],
    }


def convert_jsonl_to_glm_format(input_dir, output_dir):
    """
    将多个目录中的jsonl数据转换为glm格式
    """
    # 使用glob模块获取所有的jsonl文件路径
    jsonl_file_paths = glob.glob(input_dir + '**/*.jsonl', recursive=True)

    # 遍历每一个jsonl文件
    for jsonl_file_path in jsonl_file_paths:
        with open(jsonl_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        result_list = []

        # 遍历文件中的每一行
        # 使用tqdm迭代器
        for line in tqdm(lines, desc='Processing'):
            data = json.loads(line)

            if isinstance(data, dict):  # 若为单个字典，将 "question" 映射到 "prompt"， "response_rejected" 映射到 "response"
                formatted_dict = format_single_dict(data)
                formatted_dict["id"] = str(uuid.uuid4())
                formatted_dict["history"] = []
                formatted_dict["reference"] = ""
                result_list.append(formatted_dict)
            elif isinstance(data, list):  # 若为列表，将最后一个 "question" 映射到 "prompt"， "response_rejected" 映射到 "response"，前面的到 "history"中
                history = [format_single_dict(x) for x in data[:-1]]  # 映射前n-1个
                last = format_single_dict(data[-1])  # 映射最后一个
                
                last["id"] = str(uuid.uuid4())
                last["history"] = history
                last["reference"] = ""
                result_list.append(last)

         # 输出结果到同名的输出文件
        output_file_path = os.path.join(output_dir, os.path.basename(jsonl_file_path))
        with open(output_file_path, 'w', encoding='utf-8') as f:
            for item in result_list:
                json.dump(item, f, ensure_ascii=False)  # 添加 ensure_ascii=False 参数，确保输出格式为非ascii
                f.write('\n')


# 调用函数
same_path = 'F:/code/github/ce/'
input_dir = same_path + 'filter_multi_english_data_split'  # 输入目录路径
output_dir = input_dir + '_to_glm'  # 输出目录路径
# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
convert_jsonl_to_glm_format(input_dir, output_dir)