import jsonlines
import json
import os
from tqdm import tqdm

# 定义代码相关和中国文化相关的关键词
# V1
code_words = ["code", "python", "java", "javascript", "#", "{", "}", "for", "while", "programming", "<", ">", "/"]
china_words = ["wushu", "guzhen", "erhu", "Chinese chess", "xiangqi", "Go", "weiai", "China", "Chinese"]
translation_words = ["Translate", "translate", "interpret", "translation"]
# V2
# code_words = ["code", "python", "java", "javascript", "C++", "C#", "HTML", "<html>", "<body>", "CSS", "PHP", "Swift", "Kotlin", "Flutter", "#", "{", "}", "for", "while", "if", "else", "programming", "<", ">", "(", ")", "/", "*", "=", "+", "-", ]
# china_words = ["wushu", "guzhen", "erhu", "Chinese chess", "xiangqi", "Go", "weiai", "China", "Chinese", "Beijing", "Shanghai", "Guangzhou", "Shenzhen", "chopstick", "Peking Opera", "taichi", "kung fu", "dumpling", "spring festival", "mid-autumn", "Confucius"]
# translation_words = ["Translate", "translate", "interpret", "interpretation", "translation", "interpreter", "translator", "bilingual", "multilingual", "language", "dictionary", "vocabulary", "Chinese to English", "English to Chinese", "Cantonese", "Mandarin"]

template_responses = ["非常抱歉，我目前无法提供你需要的具体信息，如果你有其他的问题或者需要查找其他信息，我非常乐意帮助你。"]

# 定义数据文件路径
data_path = "F:\\code\\github\\ce\\glm_structured_data\\zh_en_mixed_0311_0327_5k.jsonl"
saved_dir = "F:\\code\\github\\ce\\glm_filter_saved_data"
cleaned_dir = "F:\\code\\github\\ce\\glm_filter_cleaned_data"
saved_file = "zh_en_mixed_0311_0327_5k.jsonl"
cleaned_file = "zh_en_mixed_0311_0327_5k.jsonl"
saved_path = os.path.join(saved_dir, saved_file)
cleaned_path = os.path.join(cleaned_dir, cleaned_file)

# 检查输出目录是否存在，如果不存在就创建
if not os.path.exists(saved_dir):
    os.makedirs(saved_dir)
if not os.path.exists(cleaned_dir):
    os.makedirs(cleaned_dir)

saved_count = 0
cleaned_count = 0

# 在上下文中打开数据文件
with jsonlines.open(data_path) as f, jsonlines.open(saved_path, mode='w') as fs, jsonlines.open(cleaned_path, mode='w') as fc:
    # 遍历每一行数据
    # 使用tqdm迭代器
    for item in tqdm(f, desc='Processing'):
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

print(f"Total items: {cleaned_count + saved_count}")
print(f"Cleaned items: {cleaned_count}, Ratio: {cleaned_count / (cleaned_count + saved_count):.2%}")
print(f"Saved items: {saved_count}, Ratio: {saved_count / (cleaned_count + saved_count):.2%}")