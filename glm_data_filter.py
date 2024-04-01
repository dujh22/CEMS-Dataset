import jsonlines
import os
from tqdm import tqdm

# 定义代码相关和中国文化相关的关键词

code_words = ["code", "python", "java", "javascript", "C++", "C#", "HTML", "<html>", "<body>", "CSS", "PHP", "Swift", "Kotlin", "Flutter", "#", "{", "}", "for", "while", "if", "else", "programming", "<", ">", "(", ")", "/", "*", "=", "+", "-", ]
china_words = ["wushu", "guzhen", "erhu", "Chinese chess", "xiangqi", "Go", "weiai", "China", "Chinese", "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "chopstick", "Peking Opera", "taichi", "kung fu", "dumpling", "spring festival", "mid-autumn", "Confucius"]
translation_words = ["Translate", "translate", "interpret", "interpretation", "translation", "interpreter", "translator", "bilingual", "multilingual", "language", "dictionary", "vocabulary", "Chinese to English", "English to Chinese", "Cantonese", "Mandarin"]

template_responses = ["非常抱歉，我目前无法提供你需要的具体信息，如果你有其他的问题或者需要查找其他信息，我非常乐意帮助你。"]


def process_file(data_path, saved_path, cleaned_path):
    saved_count = 0
    cleaned_count = 0

    with jsonlines.open(data_path) as f, jsonlines.open(saved_path, mode='w') as fs, jsonlines.open(cleaned_path, mode='w') as fc:
        for item in tqdm(f, desc=f'Processing {os.path.basename(data_path)}'):
            prompt = item["prompt"]
            response = item["response"]

            if any(word in prompt for word in code_words) or \
               any(word in prompt for word in china_words) or \
               any(word in prompt for word in translation_words) or \
               any(word in response for word in template_responses):
                cleaned_count += 1
                fc.write(item)
            else:
                saved_count += 1
                fs.write(item)
    
    print(f"{os.path.basename(data_path)} - Total items: {cleaned_count + saved_count}")
    print(f"Cleaned items: {cleaned_count}, Ratio: {cleaned_count / (cleaned_count + saved_count):.2%}")
    print(f"Saved items: {saved_count}, Ratio: {saved_count / (cleaned_count + saved_count):.2%}")

def main():
    input_dir = "F:\\code\\github\\ce\\glm_structured_data"
    saved_dir = "F:\\code\\github\\ce\\glm_filter_saved_data"
    cleaned_dir = "F:\\code\\github\\ce\\glm_filter_cleaned_data"

    # 检查输出目录是否存在，如果不存在就创建
    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir)
    if not os.path.exists(cleaned_dir):
        os.makedirs(cleaned_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            data_path = os.path.join(input_dir, file_name)
            saved_path = os.path.join(saved_dir, file_name)
            cleaned_path = os.path.join(cleaned_dir, file_name)

            # 跳过已经处理过的文件
            if os.path.exists(saved_path) and os.path.exists(cleaned_path):
                print(f"{file_name} 已经处理过，跳过。")
                continue

            # 执行文件处理
            process_file(data_path, saved_path, cleaned_path)

if __name__ == "__main__":
    main()
