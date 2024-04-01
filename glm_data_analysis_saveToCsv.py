import jsonlines
import os
import pandas as pd
from tqdm import tqdm

# 定义输入的jsonl文件路径和输出的csv文件路径
data_path1 = "F:\\code\\github\\ce\\glm_filter_cleaned_data\\zh_en_mixed_0311_0327_5k.jsonl"
data_path2 = "F:\\code\\github\\ce\\glm_filter_saved_data\\zh_en_mixed_0311_0327_5k.jsonl"
out_dir = "F:\\code\\github\\ce"
out_file1 = "cleaned_prompts.csv"
out_file2 = "saved_prompts.csv"
out_path1 = os.path.join(out_dir, out_file1)
out_path2 = os.path.join(out_dir, out_file2)

# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 在上下文中打开jsonl文件
def analyse(data_path, out_path):
    data_list = []

    with jsonlines.open(data_path) as f:
        # 遍历每一行数据
        # 使用tqdm迭代器
        for item in tqdm(f, desc='Processing'):
            # 获取id和prompt
            data_id = item.get('id', '')
            prompt = item.get('prompt', '')
            data_list.append([data_id, prompt])

    # 创建一个pandas.DataFrame并将其保存为.csv文件
    df = pd.DataFrame(data_list, columns=['id', 'prompt'])
    df.to_csv(out_path, index=False, encoding='utf_8_sig')

    print("Prompts extraction finished")

if __name__ == "__main__":
    analyse(data_path1, out_path1)
    analyse(data_path2, out_path2)