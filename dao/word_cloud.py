import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import csv


def getImg():
    # 读取csv文件
    csv_file = r'./file/weiborebangdata.csv'
    text_raw_data = set()  # 使用集合去重

    # 打开CSV文件并处理数据
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            text_raw = row[11]
            if text_raw.strip():
                text_raw_data.add(text_raw)

    # 分词处理
    text = " ".join(text_raw_data)
    words = jieba.cut(text)
    word_str = " ".join(words)

    # 加载蒙版图片
    mask_img = np.array(Image.open(r'C:/Users/JunHa/PycharmProjects/pythonProject/static/bingmayong.jpg'))

    # 生成词云
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        mask=mask_img,
        max_words=2000,
        width=800,
        height=600
    ).generate(word_str)

    # 显示词云
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # 保存词云图片
    wordcloud.to_file(r'C:/Users/JunHa/PycharmProjects/pythonProject/static/image/wordcloud.png')

# 调用函数
getImg()
