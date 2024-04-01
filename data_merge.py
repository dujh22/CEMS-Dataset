import os
import jsonlines
from tqdm import tqdm

def merge_data(source_folder, target_folder, target_file_name):
    # 保存合并的数据
    merged_data = {}
    
    for filename in os.listdir(source_folder):
        if filename.endswith(".jsonl"):
            with jsonlines.open(os.path.join(source_folder, filename)) as reader:
                for obj in tqdm(reader, desc='Processing'):
                    idx = obj["id"]
                    if idx not in merged_data:
                        # 若idx不存在，新建空字段
                        merged_data[idx] = {"gpt_response": "", "glm_response": ""}
                    # 更新gLm或gPt字段
                    if "gpt_response" in obj:
                        merged_data[idx]["gpt_response"] = obj["gpt_response"]
                    elif "glm_response" in obj:
                        merged_data[idx]["glm_response"] = obj["glm_response"]
                    # 更新其余字段
                    for key in obj:
                        if key not in ["gpt_response", "glm_response"]:
                            merged_data[idx][key] = obj[key]
    
    # 将合并的数据写入新文件
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    output_file = os.path.join(target_folder, target_file_name)
    with jsonlines.open(output_file, mode='w') as writer:
        for key, value in merged_data.items():
            writer.write(value)

# 调用函数
merge_data('F:\code\github\ce\glm_filter_saved_data_generate_concurrent_calibration', 'F:\code\github\ce\glm_filter_saved_data_generate_concurrent_merge', 'target_file.jsonl')