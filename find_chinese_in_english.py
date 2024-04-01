import re

def find_chinese_texts_and_sentences(text):
    """
    Find all Chinese texts and the sentences they belong to in a given text.
    """
    sentences_with_chinese = re.split(r'(?<=[.!?]) +', text)
    chinese_texts_and_sentences = []

    for sentence in sentences_with_chinese:
        chinese_texts = re.findall(r'[\u4e00-\u9fff]+', sentence)
        if chinese_texts:
           chinese_texts_and_sentences.append((chinese_texts, sentence))
        # chinese_texts_and_sentences.append((chinese_texts, sentence))

    return chinese_texts_and_sentences

def process_sentences(sentences_with_chinese):
    """
    Process each sentence based on the Chinese texts within.
    Replace all Chinese texts with 'CHINESE_TEXT'.
    """
    processed_sentences = []
    for chinese_texts, sentence in sentences_with_chinese:
        # print(chinese_texts, sentence)
        processed_sentence = sentence
        for chinese_text in chinese_texts:
            processed_sentence = processed_sentence.replace(chinese_text, 'CHINESE_TEXT', 1)
        processed_sentences.append(processed_sentence)
    
    return ' '.join(processed_sentences)

# Example usage

if __name__ == "__main__":
    text = "This is an example paragraph with in between. Another sentence with 更多中文 here."
    sentences_with_chinese = find_chinese_texts_and_sentences(text)
    processed_text = process_sentences(sentences_with_chinese)
    print(processed_text)
