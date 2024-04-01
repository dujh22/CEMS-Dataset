import json
import concurrent.futures
from openai import OpenAI
import os
from tqdm import tqdm
import time

# GLM API密钥和基本URL
api_key = "QGqhzEef29eGMA5buGB9JRrUdSweTCMe2Kcg4TGDdjGqwkJFLGW2h56Fccq86rYB"
base_url = "https://api.chatglm.cn/v1"

# 初始化GLM客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 为了处理异常并在遇到失败时重试最多十次，我们可以在process_entry函数中添加异常处理逻辑。具体地说，将在调用GLM接口的部分添加一个循环，该循环最多尝试十次。如果所有尝试都失败，则捕获异常并允许代码继续执行，跳过当前的数据点。也将添加一些日志输出，以便跟踪哪些数据点被跳过。
def process_entry(data):
    history = data.get('history', [])
    prompt = data.get('prompt', '')
    data_id = data.get('id', '')
    # print(data_id)

    # 构造messages
    messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": h['prompt'] if i % 2 == 0 else h['response']} for i, h in enumerate(history)]
    messages.append({"role": "user", "content": prompt})

    attempts = 0
    while attempts < 10:
        try:
            # 调用GLM接口
            stream = client.chat.completions.create(messages=messages, model="chatglm3-32b-v0.8-data", temperature=0.95, top_p=0.7, stream=True, max_tokens=1024)
            glm_response = ''.join(part.choices[0].delta.content or "" for part in stream)

            # 添加GLM响应到数据并返回
            data['glm_response'] = glm_response
            return data
        except Exception as e:
            print(f"在处理 {data_id} 时遇到异常：{e}")
            attempts += 1
            print(f"重试次数 {attempts}/10")
    
    print(f"跳过数据点 {data_id}，因为尝试了10次都失败了。")
    # 返回一个修改过的版本，其中包含错误信息，而不是简单地跳过，以便在输出文件中记录这一点。
    data['glm_response'] = "Error: Failed after 10 attempts"
    return data


def process_jsonl_concurrently(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data_list = [json.loads(line) for line in infile]

    total = len(data_list)

    # 使用tqdm创建进度条
    with tqdm(total=total, desc="正在处理") as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_entry, data) for data in data_list]
            
            results = []
            for future in concurrent.futures.as_completed(futures):
                # 每完成一个任务，进度条更新一次
                results.append(future.result())
                pbar.update(1)
        
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for result in results:
            json.dump(result, outfile, ensure_ascii=False)
            outfile.write('\n')



# 实例：调用函数处理文件
# out_dir = "F:\code\github\ce\glm_filter_saved_data_generate_concurrent"
# # 检查输出目录是否存在，如果不存在就创建
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)            
# process_jsonl_concurrently('F://code//github//ce//filter_ce_data_split_to_glm//train-00000-of-00001.parquet.jsonl', 'F://code//github//ce//filter_ce_data_split_to_glm//filter_ce_data_split_to_glm_train-00000-of-00001.parquet.jsonl')
    
def main():
    input_dir = 'F://code//github//ce//data_has_batch'
    output_dir = 'F://code//github//ce//data_has_batch_has_generate'

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            print(f"正在处理文件：{input_file_path}")
            process_jsonl_concurrently(input_file_path, output_file_path)
            print(f"处理完成，输出文件：{output_file_path}")

            # 暂停30秒，并打印倒计时
            print("等待30秒...")
            for i in range(30, 0, -1):
                # 打印倒计时，使用end='\r'来确保在同一行更新计时
                print(f"继续下一个文件处理还有：{i}秒", end='\r')
                time.sleep(1)
            print()  # 打印一个新行，为了之后的输出不会在同一行

if __name__ == "__main__":
    main()