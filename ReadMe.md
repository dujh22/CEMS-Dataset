# 构造中英混杂任务数据集

针对不同数据来源会有不同的pipeline

## GLM的LOG数据集

- ### 数据结构化

  - 目标：将LOG数据集结构转化为GLM通用结构
  - ```shell
    python glm_data_structure.py
    ```
- ### 数据过滤

  - 目标：初步过滤掉代码类、中国类、翻译类和模板类的prompt
  - ```shell
    python glm_data_filter.py
    ```
- ### 数据提取

  - 后续步骤和开源数据集一致
  - 注意过滤后F://code//github//ce//glm_filter_saved_data文件夹的数据拷贝到 F://code//github//ce//data_has_batch_has_generate

## 开源数据集

- ### 数据收集

  - 请将数据集下载链接放在data_url.txt文件中，每行一个url，参照目前data_url.txt文件内格式
  - 翻墙
  - 多次运行如下命令，直到全部数据集下载完成

    ```shell
    python data_download.py
    ```
  - 数据会被保存在raw_data中
- ### 数据格式统一

  - 目标：需要针对不同的数据来源进行格式统一脚本的书写/升级
- ### 数据生成

  - 目标：利用开源数据集中的prompt依次测试glm模型生成的response
  - ```
    python use_glm_api_for_glm_generate_concurrent.py
    ```
- ### 数据提取

  - 目标：将开源数据集转化为glm数据集格式，清洗掉prompt不是英文的，一定程度清洗掉可能涉及代码类或者翻译类的prompt，保证glm生成的response中含有中文。
  - ```shell
    python data_extract.py 
    ```

    （可在上一步数据生成同时进行，但注意上一步数据生成执行完后务必执行此指令确保全部数据均进行了提取）
- ### 数据修改

  - 目标：将glm对应的response中中文的部分修改为英文
  - ```
    python use_gpt_api_for_glm_generate_concurrent_modifyV3.py 
    ```

    （可在上一步数据提取后立刻进行，但注意上两步数据生成执行完后务必执行数据提取后执行此指令确保全部数据均进行了修改）
- ### 数据集成

  - 目标：将修改文件夹内的全部文件集成到一个jsonl文件中
  - ```
    python data_merge.py
    ```
- ### 数据选择

  - 目标：移除json中的无关字段
  - ```
    python data_choice.py
    ```
- ### 计算比率

  - 目标：计算数据集质量衡量指标，主要有两个维度。一个维度是重叠率，也就是 gpt3_modify_response 和 response字段的字符串匹配长度占response总长的比例，然后所有的json取平均，最大值，和最小值输出；另一个维度是纯英文率/中文字符占比，也就是统计gpt3_modify_response 字段中中文字符占的比例，然后所有的json取平均，最大值，和最小值输出；同样统计response字段中中文字符占的比例，然后所有的json取平均，最大值，和最小值输出；同样统计prompt字段中中文字符占的比例，然后所有的json取平均，最大值，和最小值输出。
  - ```shell
    python CalculationOfTheOverlapRate.py
    ```

## 特别说明

- 注意首先配置环境 pip install -r requirements.txt
  - 其中特别注意针对glm使用的openai版本是最新的，针对gpt使用的openai版本是0.28.0，所以需要安装两个环境
  -
