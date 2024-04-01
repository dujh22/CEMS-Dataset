import os
import json

def batch_split_jsonl(input_dir, output_dir, batch_size=1000):
    # 创建输出文件夹，如果它不存在的话
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.jsonl'):
            path = os.path.join(input_dir, filename)
            with open(path, 'r', encoding='utf-8') as file:
                batch = []
                batch_number = 1
                for line in file:
                    batch.append(json.loads(line))
                    if len(batch) == batch_size:
                        # 保存当前批次的数据到一个新文件
                        output_filename = f"{filename[:-6]}_{batch_number}.jsonl"
                        # 实现原理是将filename原始文件名去掉后缀（.jsonl），然后将其与batch_number拼接成一个新文件名，最后加上新的后缀.jsonl。
                        with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as output_file:
                            for item in batch:
                                output_file.write(json.dumps(item, ensure_ascii=False) + '\n')
                        batch = []
                        batch_number += 1
                # 保存最后一个不满batch_size的批次（如果有的话）
                if batch:
                    output_filename = f"{filename[:-6]}_{batch_number}.jsonl"
                    with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as output_file:
                        for item in batch:
                            output_file.write(json.dumps(item, ensure_ascii=False) + '\n')

# 使用示例
input_dir = 'F://code//github//ce//data_wait_to_batch'  # 输入文件夹路径
output_dir = 'F://code//github//ce//data_has_batch'  # 保存分批文件的文件夹路径
batch_split_jsonl(input_dir, output_dir)
