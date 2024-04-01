import jsonlines
import json
import re
import os
from tqdm import tqdm

# 定义数据文件路径
data_path = "F:\\code\\github\\ce\\glm_raw_data\\zh_en_mixed_0311_0327_5k.jsonl"
out_dir = "F:\\code\\github\\ce\\glm_structured_data"
out_file = "zh_en_mixed_0311_0327_5k.jsonl"
out_path = os.path.join(out_dir, out_file)

# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# 在上下文中打开数据文件
with jsonlines.open(data_path) as f, jsonlines.open(out_path, mode='w') as fo:
    # 遍历每一行数据
    # 使用tqdm迭代器
    for item in tqdm(f, desc='Processing'):
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

print("Finished data restructuring")