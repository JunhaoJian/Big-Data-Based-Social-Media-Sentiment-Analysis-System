import pandas as pd


def getCommentsList(file_path1):
    # 读取 CSV 文件
    df = pd.read_csv(file_path1)

    # 去除特定内容及相关字段
    filtered_df = df[df['content'] != "用户未点评，系统默认好评。"]

    # 创建字典
    comments_list = filtered_df[['commenter', 'commenter_city', 'content','sentiment']].to_dict(orient='records')

    return comments_list


# 调用函数并获取数据
comments = getCommentsList('./predictive/bingmayong1_with_sentiment.csv')

