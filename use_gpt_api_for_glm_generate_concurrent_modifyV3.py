import json
import openai
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor
import re
import config

# GPT API密钥和基本URL
api_key = config.GPT_API_KEY
base_url = config.GPT_BASE_URL

promt1 = "Given "
promt2 = ", translate it into English, returning {\"English texts\":\"\"}."

# 设定API密钥和基本URL
openai.api_key = api_key
openai.api_base = base_url 

def find_chinese_texts_and_sentences(text):
    # 初始化变量
    current_sentence = ""
    chinese_texts_and_sentences = []

    # 逐个字符扫描文本
    for char in text:
        # 将字符添加到当前句子
        current_sentence += char
        # 如果遇到句子结束的标点
        if char in ".!?":
            # 检查当前句子是否包含中文字符，并收集中文文本
            chinese_texts = re.findall(r'[\u4e00-\u9fff]+', current_sentence)
            # 注意这里chinese_texts已经是一个包含所有中文字符串的列表
            chinese_texts_and_sentences.append((chinese_texts, current_sentence))
            # 重置当前句子
            current_sentence = ""
    # 检查并处理最后一个句子（如果它不以分句标点结束）
    if current_sentence:
        chinese_texts = re.findall(r'[\u4e00-\u9fff]+', current_sentence)
        chinese_texts_and_sentences.append((chinese_texts, current_sentence))

    return chinese_texts_and_sentences


def process_line(line):
    try:
        data = json.loads(line)
        response = data.get('response', '')
        
        sentences_with_chinese = find_chinese_texts_and_sentences(response)
        
        processed_sentences = []
        for chinese_texts, sentence in sentences_with_chinese:
            if not chinese_texts:
                processed_sentences.append(sentence)
                continue
            processed_sentence = sentence
            for chinese_text in chinese_texts:
                last_prompt = promt1 + json.dumps({"Chinese texts": chinese_text}, ensure_ascii=False) + promt2
                messages = [{"role": "user", "content": last_prompt}]
                english_text = ''
                for i in range(5):
                    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
                    gpt_response = chat_completion.choices[0].message.content
                    try:
                        new_response = json.loads(gpt_response)
                        english_text = new_response.get('English texts', '')
                        if english_text:
                            english_text = english_text.lower() # 转换为小写
                            break
                    except:
                        continue
                
                # 首先处理中文串后面不必要的(***)
                chinese_text_start = processed_sentence.find(chinese_text)
                # 考虑括号前的空格
                left_bracket_pos = chinese_text_start + len(chinese_text)
                while left_bracket_pos < len(processed_sentence) and processed_sentence[left_bracket_pos] == ' ': 
                    left_bracket_pos += 1 
                if left_bracket_pos < len(processed_sentence) and processed_sentence[left_bracket_pos] in ['(', '（']:
                    right_bracket_pos = left_bracket_pos + 1
                    for i in range(left_bracket_pos + 1, len(processed_sentence)):
                        if processed_sentence[i] in [')', '）']:
                            right_bracket_pos = i
                            break 
                    if right_bracket_pos < len(processed_sentence):  
                        right_bracket_pos = right_bracket_pos + 1
                    else:
                        right_bracket_pos = left_bracket_pos
                    # 判断替换字段前后是否需要添加空格
                    # 前面的空格
                    if chinese_text_start == 0:
                        english_text = english_text[0].upper() + english_text[1:]  # 首字母大写
                    else:
                        english_text = ' ' + english_text
                    # 后面的空格
                    if chinese_text_start + len(chinese_text) < len(processed_sentence) and processed_sentence[chinese_text_start + len(chinese_text)] != ' ':
                        english_text += ' '
                    # 拼接
                    processed_sentence = processed_sentence[:chinese_text_start] +  english_text + processed_sentence[right_bracket_pos:]  
                else:
                    # 只判断替换字段前后是否需要添加空格
                    # 前面的空格
                    if chinese_text_start == 0:
                        english_text = english_text[0].upper() + english_text[1:]  # 首字母大写
                    else:
                        english_text = ' ' + english_text
                    # 后面的空格
                    if chinese_text_start + len(chinese_text) < len(processed_sentence) and processed_sentence[chinese_text_start + len(chinese_text)] != ' ':
                        english_text += ' '
                    # 拼接
                    processed_sentence = processed_sentence[:chinese_text_start] +  english_text + processed_sentence[chinese_text_start + len(chinese_text):]
                
            processed_sentences.append(processed_sentence)
        data['gpt3point5turbo_modify_response'] = ' '.join(processed_sentences)
        # 判断其中是否有长度大于1的空格，如果有全部替换为长度为1
        data['gpt3point5turbo_modify_response'] = ' '.join(data['gpt3point5turbo_modify_response'].split(' '))
    except Exception as ex:
        print(f'An error occurred: {ex}')
        data = None
    
    return data


def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        lines = list(tqdm(infile, desc='Processing'))

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(tqdm(executor.map(process_line, lines), total=len(lines)))

        for data in results:
            if data is not None:  # 只有当 data 不为 None 时才写入文件
                json.dump(data, outfile, ensure_ascii=False)
                outfile.write('\n')

# 实例：调用函数处理文件
# out_dir = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify"
# if not os.path.exists(out_dir):
#     os.makedirs(out_dir)

# input_file = "F:\\code\\github\\ce\\glm_filter_saved_data_generate_concurrent_merge_modify\\target_file_gpt3point5turbo21.jsonl"
# output_file = os.path.join(out_dir, "target_file_gpt3point5turbo22.jsonl")
# process_jsonl(input_file, output_file)

# # 检测有多少个data拥有了gpt3point5turbo_modify_response属性
# count = 0
# sum = 0
# with open(output_file, 'r', encoding='utf-8') as f:
#     for line in f:
#         data = json.loads(line)
#         if data.get('gpt3point5turbo_modify_response', '') != '':
#             count += 1
#         sum += 1
# print(f"有{count}个data拥有了gpt3point5turbo_modify_response属性")
# print(f"共计有{sum}个data")

def main():
    input_dir = 'F://code//github//ce//data_has_batch_has_generate_has_extract'
    output_dir = 'F://code//github//ce//data_has_batch_has_generate_has_extract_has_modify'

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 遍历输入目录中的所有jsonl文件
    for file_name in tqdm(os.listdir(input_dir), desc="处理文件"):
        if file_name.endswith('.jsonl'):
            input_file_path = os.path.join(input_dir, file_name)
            output_file_path = os.path.join(output_dir, file_name)

            # 如果输出文件已存在，则跳过处理
            if os.path.exists(output_file_path):
                print(f"{file_name} 已存在，跳过处理。")
                continue

            # 执行处理逻辑
            process_jsonl(input_file_path, output_file_path)

            # 统计拥有特定属性的data数量
            count = 0
            sum = 0
            with open(output_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    if data.get('gpt3point5turbo_modify_response', '') != '':
                        count += 1
                    sum += 1

            print(f"{file_name}: 有{count}个data拥有了gpt3point5turbo_modify_response属性，共计有{sum}个data")

if __name__ == "__main__":
    main()