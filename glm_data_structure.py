import jsonlines
import json
import re
import os
from tqdm import tqdm

def process_file(data_path, out_path):
    # 在上下文中打开数据文件
    with jsonlines.open(data_path) as f, jsonlines.open(out_path, mode='w') as fo:
        # 遍历每一行数据
        # 使用tqdm迭代器
        for item in tqdm(f, desc=f'Processing {os.path.basename(data_path)}'):
            # 初始化历史对话列表
            history = []

            # 从final_prompt中正则匹配出历史对话
            final_prompt = item["output"]["final_prompt"]
            
            rounds = final_prompt.split('##第')[1:]
            for r in rounds:
                p = re.search(r'问：(.*?)\n\n答：', r, re.S)
                t = re.search(r'答：(.*)', r, re.S)
                if p and t:
                    history.append({"prompt": p.group(1), "response": t.group(1)})

            # 检查并移除历史中与prompt相同且无response的item
            if history and history[-1]['prompt'] == item["input"]["prompt"] and not history[-1]['response']:
                history.remove(history[-1])

            # 提取参考文本
            reference_pos = final_prompt.find('##第 1 轮##')
            if reference_pos != -1:
                reference = final_prompt[:reference_pos]
            else:
                reference = final_prompt

            # 创建新的数据结构
            structured = {
                "id": item.get("id", ""), # 该ID不一定存在于所有数据中
                "history": history,
                "prompt": item["input"]["prompt"],
                "response": item["output"]["text"][0],
                "reference": reference,
            }

            # 将结构化数据写入到新文件中
            fo.write(structured)

def main():
    input_dir = 'F:\\code\\github\\ce\\glm_raw_data'
    output_dir = 'F:\\code\\github\\ce\\glm_structured_data'

    # 检查输出目录是否存在，如果不存在就创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            data_path = os.path.join(input_dir, file_name)
            out_path = os.path.join(output_dir, file_name)

            # 如果输出文件已存在，则跳过处理
            if os.path.exists(out_path):
                print(f"{file_name} 已存在，跳过处理。")
                continue

            # 执行处理逻辑
            process_file(data_path, out_path)

    print("Finished data restructuring for all files")

if __name__ == "__main__":
    main()
