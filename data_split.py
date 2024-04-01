import re
import json
import os
from tqdm import tqdm

# 过滤问题文本，根据要求去除特定的关键词和模式
def filter_question(question_data):
    question = question_data['question']

    # 关键词列表
    keywords = ["teach", "japanese", "chinese", "translate", "code", "file", "url"]
    # 代码关键词列表
    programming_keywords = ["for", "while", "if", "else", "switch", "case", "try", "except", 
                            "class", "def", "with", "return", "break", "continue", "public", 
                            "private", "protected", "import", "from", "as", "int", "float", 
                            "double", "char", "boolean", "string", "new", "extends", "implements", 
                            "void", "enum", "print"]

    # 正则表达式模式匹配超链接
    question = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', question)

    # 剔除问题中包含的关键词
    for keyword in keywords:
        if keyword in question:
            question = ''

    # 剔除问题中包含的代码关键词
    for code_keyword in programming_keywords:
        if code_keyword in question:
            question = ''

    question_data['question'] = question.strip()
    return question_data

# 处理单轮对话数据集
def process_single_turn_data(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.readlines()

            filtered_questions = []  # 过滤后的问题

            # 过滤问题并保存
            # 使用tqdm迭代器
            for line in tqdm(data, desc='Processing'):
                question_data = json.loads(line)
                filtered_question = filter_question(question_data)
                # 如果question字段不为空
                if filtered_question['question']:
                    filtered_questions.append(filtered_question)

            # 保存问题
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(json.dumps(question, ensure_ascii=False) for question in filtered_questions))

# 处理多轮对话数据集
def process_multi_turn_data(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.readlines()

            filtered_questions = []  # 过滤后的问题

            # 过滤问题并保存
            # 使用tqdm迭代器
            for line in tqdm(data, desc='Processing'):
                question_data = json.loads(line)
                filtered_question = [filter_question(q_data) for q_data in question_data]
                # 如果列表所有的json的question字段不为空
                if all(q_data['question'] for q_data in filtered_question):
                    filtered_questions.append(filtered_question)

            # 保存问题
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(json.dumps(question, ensure_ascii=False) for question in filtered_questions))

# 使用示例
base_folder = 'F:/code/github/ce/filter_ce_data'
process_single_turn_data(base_folder, base_folder + '_split')

base_folder_multi = 'F:/code/github/ce/filter_multi_ce_data'
process_multi_turn_data(base_folder_multi, base_folder_multi + '_split')

base_folder = 'F:/code/github/ce/filter_english_data'
process_single_turn_data(base_folder, base_folder + '_split')

base_folder_multi = 'F:/code/github/ce/filter_multi_english_data'
process_multi_turn_data(base_folder_multi, base_folder_multi + '_split')