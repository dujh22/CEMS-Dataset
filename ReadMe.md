# 构造中英混杂任务数据集

针对不同数据来源会有不同的pipeline

## 开源数据集

- step1：数据收集
  - 请将数据集下载链接放在data_url.txt文件中，每行一个url，参照目前data_url.txt文件内格式
  - 翻墙
  - 多次运行 `python data_download.py` ，直到全部数据集下载完成
  - 数据会被保存在raw_data中

​			

## 特别说明

- 注意首先配置环境 pip install -r requirements.txt
  - 其中特别注意针对glm使用的openai版本是最新的，针对gpt使用的openai版本是0.28.0，所以需要安装两个环境
  - 