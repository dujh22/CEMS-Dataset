# 文件说明
# 1. 该文件用于处理标准化数据的拆分，根据数据中的问题类型和回答类型进行过滤。
# 2. 标准化数据包含四个文件夹：standardized_data、filter_english_data、filter_ce_data、filter_multi_english_data、filter_multi_ce_data。


import os
import json
import jsonlines
import shutil
from detect_string_type import judge_language
from tqdm import tqdm
import time

def handle_jsonl_file(filepath, dest_folder1, dest_folder2, dest_folder3, dest_folder4):
    collection1 = []
    collection2 = []
    collection3 = []
    collection4 = []
    
    with jsonlines.open(filepath, mode='r') as reader:
        # 使用tqdm迭代器
        for temp in tqdm(reader, desc='Processing'):
            if isinstance(temp, list):
                if len(temp) == 1:
                    obj = temp[0]
                else:
                    obj = temp
            else:
                obj = temp
            
            if isinstance(obj, dict):
                question = obj.get('question')
                response_chosen = obj.get('response_chosen')
                if judge_language(question) == 'en':
                    if judge_language(response_chosen) == 'en':
                        collection1.append(obj)
                    else:
                        collection2.append(obj)
            elif isinstance(obj, list):
                questions = [item.get('question') for item in obj]
                responses = [item.get('response_chosen') for item in obj]
                if all(judge_language(q) == 'en' for q in questions):
                    if all(judge_language(r) == 'en' for r in responses):
                        collection3.append(obj)
                    else:
                        collection4.append(obj)

    # 写入到目标文件    
    with jsonlines.open(os.path.join(dest_folder1, os.path.basename(filepath)), mode='w') as writer:
        writer.write_all(collection1)

    with jsonlines.open(os.path.join(dest_folder2, os.path.basename(filepath)), mode='w') as writer:
        writer.write_all(collection2)
    
    with jsonlines.open(os.path.join(dest_folder3, os.path.basename(filepath)), mode='w') as writer:
        writer.write_all(collection3)

    with jsonlines.open(os.path.join(dest_folder4, os.path.basename(filepath)), mode='w') as writer:
        writer.write_all(collection4)


def process_standardized_data():
    src_folder = 'standardized_data'
    dest_folder1_1 = 'filter_english_data'
    dest_folder1_2 = 'filter_ce_data'
    dest_folder2_1 = 'filter_multi_english_data'
    dest_folder2_2 = 'filter_multi_ce_data'
    
    os.makedirs(dest_folder1_1, exist_ok=True)
    os.makedirs(dest_folder1_2, exist_ok=True)
    os.makedirs(dest_folder2_1, exist_ok=True)
    os.makedirs(dest_folder2_2, exist_ok=True)

    for file_name in os.listdir(src_folder):
        if file_name.endswith('.jsonl'):
            full_path = os.path.join(src_folder, file_name)
            print("正在处理{}...".format(file_name))
            handle_jsonl_file(full_path, dest_folder1_1, dest_folder1_2, dest_folder2_1, dest_folder2_2)

if __name__ == '__main__':
    process_standardized_data()