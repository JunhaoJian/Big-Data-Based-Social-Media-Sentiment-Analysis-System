import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from pymysql import connect
def getImg():
    # 连接数据库
    conn = connect(host='localhost', port=3306, user='root', password='123456', database='weibo', charset='utf8mb4')
    cursor = conn.cursor()

    # 查询数据库中的username字段
    sql = "SELECT username FROM weibo"
    cursor.execute(sql)
    data = cursor.fetchall()

    # 提取username字段并去重
    usernames = [row[0] for row in data]
    unique_usernames = list(set(usernames))  # 去除重复的博主

    # 分词处理
    text = " ".join(unique_usernames)
    words = jieba.cut(text)
    word_str = " ".join(words)

    # 生成词云
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        background_color=None,
        mode='RGBA',
        max_words=2000,
        width=800,
        height=600
    ).generate(word_str)

    # 显示词云
    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    # 保存词云图片，确保以PNG格式保存透明背景
    wordcloud.to_file('../static/image/dapingwordcloud1.png')

    # 关闭数据库连接
    cursor.close()
    conn.close()

# 调用函数
getImg()
