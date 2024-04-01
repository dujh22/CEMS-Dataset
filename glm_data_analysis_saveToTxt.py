# 函数功能：从jsonl文件中提取prompt并进行分析，结果写入到txt文件中

import jsonlines
import os
from tqdm import tqdm

# 定义输入的jsonl文件路径和输出的txt文件路径
data_path1 = "F:\\code\\github\\ce\\glm_filter_cleaned_data\\zh_en_mixed_0311_0327_5k.jsonl"
data_path2 = "F:\\code\\github\\ce\\glm_filter_saved_data\\zh_en_mixed_0311_0327_5k.jsonl"
out_dir = "F:\\code\\github\\ce"
out_file1 = "cleaned_prompts.txt"
out_file2 = "saved_prompts.txt"
out_path1 = os.path.join(out_dir, out_file1)
out_path2 = os.path.join(out_dir, out_file2)

# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 在上下文中打开jsonl文件
def analyse(data_path, out_path):
    with jsonlines.open(data_path) as f, open(out_path, 'w', encoding='utf-8') as fo:
        # 遍历每一行数据
        # 使用tqdm迭代器
        for item in tqdm(f, desc='Processing'):
            # 获取prompt并写入到txt文件中
            id = item.get('id', '')
            prompt = item.get('prompt', '')
            fo.write(f"{id}------>{prompt}\n")

    print("Prompts extraction finished")

if __name__ == "__main__":
    analyse(data_path1, out_path1)
    analyse(data_path2, out_path2)
