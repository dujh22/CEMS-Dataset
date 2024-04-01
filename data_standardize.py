# Function: 标准化数据集，将原始数据集转换为标准化的数据集

import os
import json
import pandas as pd
import pyarrow.parquet as pq


question_set = set() # 用于存放问题集合

def create_object(question, response_chosen, response_rejected):
    return {
            "question": question, 
            "response_chosen": response_chosen, 
            "response_rejected": response_rejected
        }

# 这一部分是针对不同数据集的处理函数
# 代表性数据集，多轮对话 + json格式
def openchat_openchat_sharegpt4_dataset(file_path):
    data_standard = []
    data = pd.read_json(file_path) 
    print(data.count())
    print('\n\n')
    question_set = set()
    for index, row in data.iterrows():
        dialog = row["items"]
        obj_merge = []
        for i in range(0, len(dialog), 2): # 扫描所有的对话条目，步长为2
            if dialog[i]['from'] == 'human':
                question = dialog[i]['value']
                response_chosen = dialog[i+1]['value'] if i+1 < len(dialog) and dialog[i+1]['from'] == 'gpt' else ""
                response_rejected = ""
                obj = create_object(question, response_chosen, response_rejected)
                obj_merge.append(obj)
        if obj_merge[0]["question"] not in question_set: # 如果问题集合中不存在当前问题，则添加到数据集中
            data_standard.append(obj_merge)
            question_set.add(obj_merge[0]["question"])
    return data_standard

# 代表性数据集，单轮对话 + parquet格式
def abhinand_alpaca_gpt4_sharegpt(file_path):
    data_standard = []
    data = pd.read_parquet(file_path)
    print(data.count())
    print('\n\n')
    for i in range(data['conversations'].size):
        question = [item['value'] for item in data['conversations'][i] if item['from']=='human'][0]
        response_chosen = [item['value'] for item in data['conversations'][i] if item['from']=='gpt'][0]
        # 当前的转换逻辑不涉及到response_rejected，所以暂且赋予一个空字符串值
        response_rejected = ""
        obj = create_object(question, response_chosen, response_rejected)
        if question not in question_set: # 如果问题集合中不存在当前问题，则添加到数据集中
            data_standard.append(obj)
            question_set.add(question)
    return data_standard

# 递归扫描文件夹, 找到所有指定后缀的文件
def recursive_file_scan(dir_path, exts=('.txt', '.json', '.jsonl', '.parquet')):
    files_to_process = []
    for root, dir, files in os.walk(dir_path):
        for file in files:
            if file.endswith(exts):
                print(f"Detected file: {file}")
                process_file = input("Process this file? Enter 'y' for yes and 'n' for no: ")
                if process_file.lower() == 'y':
                    files_to_process.append(os.path.join(root, file))
                print('\n\n')
    return files_to_process

def convert_to_standard(file):
    # 存放数据标准化后的数据集
    data_standard = []
    
    # 对应数据集标准化，具体实现取决于原始数据的格式
    if 'openchat_openchat_sharegpt4_dataset' in file:
        data_standard = openchat_openchat_sharegpt4_dataset(file)
    elif 'abhinand_alpaca_gpt4_sharegpt' in file:
        data_standard = abhinand_alpaca_gpt4_sharegpt(file)
    else:
        print("Unknown dataset")

    # 返回标准化后的数据集
    return data_standard

def save_standard_data(data_standard, output_dir, output_filename):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as fout:
        for item in data_standard:
            fout.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    dir_path = './raw_data'
    output_dir = './standardized_data'
    
    data_files = recursive_file_scan(dir_path)
    
    for file in data_files:
        data_standard = convert_to_standard(file)
        output_filename = os.path.basename(file) + '.jsonl'
        save_standard_data(data_standard, output_dir, output_filename)
    
if __name__ == "__main__":
    main()