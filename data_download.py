# 文件说明
# 批量下载 Hugging Face 上的数据集
# 数据集链接存储在 data_urls.txt 文件中，一行一个链接
# 下载后的数据集保存在对应的文件夹中，文件夹名根据链接自动生成

from pycrawlers import huggingface
# 实例化类
# token
token = ''
hg = huggingface(token=token)

# urls = ['https://huggingface.co/datasets/openchat/openchat_sharegpt4_dataset/tree/main',
#         'https://huggingface.co/datasets/abhinand/alpaca-gpt4-sharegpt/tree/main']
# 从txt文件中读取URL列表
with open('data_urls.txt', 'r') as f:
    urls = [line.strip() for line in f]
            
# 批量下载
# 默认保存位置在当前脚本所在文件夹 ./
# hg.get_batch_data(urls)
# 自定义下载位置
# paths = ['F:/data/openchat_sharegpt4_dataset', 'F:/data/alpaca-gpt4-sharegpt/']
base_url = 'https://huggingface.co/datasets/'
suffix = '/tree/main'
paths = ['F:/code/github/ce/raw_data/' + url.replace(base_url, '').replace(suffix, '').replace('/', '_').replace('-', '_') for url in urls]

# 批量下载
hg.get_batch_data(urls, paths)