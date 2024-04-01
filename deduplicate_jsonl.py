import json
import os

def deduplicate_jsonl(file_name):
    # 使用 dict 来存储每个 id 只出现一次的 json 对象
    unique_id_dict = {}

    removed_count = 0

    with open(file_name, 'r', encoding='utf-8') as jsonl_file:
        # 每次读取文件的一行
        for line in jsonl_file:
            json_obj = json.loads(line)
            internal_id = json_obj['internal_id']

            # 如果 id 在 unique_id_dict 中不存在，加入到 unique_id_dict 中
            if internal_id not in unique_id_dict:
                unique_id_dict[internal_id] = json_obj
            else:  # 如果存在，则视为重复，移除并计数
                removed_count += 1

    # 将删除后的数据写回文件
    with open(file_name, 'w', encoding='utf-8') as jsonl_file:
        for unique_json_obj in unique_id_dict.values():
            jsonl_file.write(f"{json.dumps(unique_json_obj)}\n")

    print(f"Removed {removed_count} duplicate items.")

# 替换为jsonl 文件路径
deduplicate_jsonl('C:/Users/13969/Downloads/0311_0327_5k_新平台input(1).jsonl')