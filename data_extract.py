import os
import json
import re

def is_pure_english(text):
    return re.match(r'^[a-zA-Z0-9\s\.,?!\'\"-]*$', text) is not None

def contains_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text) is not None

def is_translation_or_code_related(prompt):
    keywords = ["翻译", "代码", "sql", "bash", "arduino", "code", "python", "java", "javascript", "c++", "c#", "html", "<html>", "<body>", "css", "php", "swift", "kotlin", "flutter", "#", "{", "}", "for", "while", "if", "else", "programming", "<", ">", "(", ")", "/", "*", "=", "+", "-", "translate", "interpret", "interpretation", "translation", "interpreter", "translator", "bilingual", "multilingual", "language", "dictionary", "vocabulary", "chinese to english", "english to chinese", "cantonese", "mandarin"]
    return any(keyword in prompt.lower() for keyword in keywords)

def process_files(input_file, target_file):
    with open(target_file, 'w', encoding='utf-8') as output_file, open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data = json.loads(line)
                prompt = data.get("prompt", "")
                glm_response = data.get("glm_response", "")
                if (is_pure_english(prompt) and not is_translation_or_code_related(prompt) and contains_chinese(glm_response)):
                    data['raw_response'] = data.get('response')
                    data['response'] = data.get('glm_response')
                    json.dump(data, output_file, ensure_ascii=False)
                    output_file.write('\n')
            except json.JSONDecodeError:
                continue

def main():
    input_dir = "F://code//github//ce//data_has_batch_has_generate_has_modify"
    output_dir = "F://code//github//ce//data_has_batch_has_generate_has_modify_has_extract"

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            # 调用处理函数
            print(f"正在处理文件：{input_file_path}")
            process_files(input_file_path, output_file_path)  # 注意调整为正确的函数名
            print(f"处理完成，输出文件：{output_file_path}")

if __name__ == "__main__":
    main()
