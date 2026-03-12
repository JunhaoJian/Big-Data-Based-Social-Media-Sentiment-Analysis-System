import pandas as pd
from dao.getPublicData import *
from db import querys
import os

def getDaPingData():
    # 生成 CSV 文件的绝对路径
    csv_file_path = 'C:\\Users\\JunHa\\Desktop\\pythonProject\\file\\weiborebangdata.csv'

    # 读取 weibo 数据
    df = pd.read_csv(csv_file_path, encoding='utf-8-sig')

    # 处理 hot_weibo_count 列，确保其为数值类型
    df['hot_weibo_count'] = pd.to_numeric(df['hot_weibo_count'], errors='coerce')

    # 统计 follower_count 超过 1000 万的用户数量
    total_follower_over_10m = df[df['follower_count'] > 10000000].shape[0]

    # 统计 hot_weibo_likes 的最大值
    max_hot_weibo_likes = df['hot_weibo_likes'].max()

    # 获取 hot_weibo_count 最大的前 100 条记录
    top_hot_weibo = df.nlargest(100, 'hot_weibo_count')[['user', 'hot_weibo_count']]

    # 分别提取 xData2 和 yData2
    xData2 = top_hot_weibo['user'].tolist()
    yData2 = top_hot_weibo['hot_weibo_count'].tolist()

    # 计算不同粉丝数量区间的博主数量
    followerList = {
        '2M-4M': df[(df['follower_count'] >= 2000000) & (df['follower_count'] < 4000000)].shape[0],
        '4M-6M': df[(df['follower_count'] >= 4000000) & (df['follower_count'] < 6000000)].shape[0],
        '6M-8M': df[(df['follower_count'] >= 6000000) & (df['follower_count'] < 8000000)].shape[0],
        '8M-10M': df[(df['follower_count'] >= 8000000) & (df['follower_count'] < 10000000)].shape[0],
        '10M+': df[df['follower_count'] > 10000000].shape[0],
    }

    # 将字典转换为列表形式
    followerList_list = list(followerList.values())

    # 获取去重后的用户和对应的粉丝数
    unique_users = df.drop_duplicates(subset='user')[
        ['user', 'follower_count', 'attitudes_count', 'comments_count', 'reposts_count']]
    xData3 = unique_users['user'].tolist()
    yData3 = unique_users['follower_count'].tolist()

    # 获取 xData4 和 yData4 系列数据
    xData4 = unique_users['user'].tolist()
    yData4_1 = unique_users['attitudes_count'].tolist()
    yData4_2 = unique_users['comments_count'].tolist()
    yData4_3 = unique_users['reposts_count'].tolist()

    allUserList = getAllUser()  # 直接获取所有用户的列表
    userDic = {}
    for i in allUserList:  # 遍历 allUserList
        if userDic.get(i[-1], -1) == -1:
            userDic[i[-1]] = 1
        else:
            userDic[i[-1]] += 1
    # print(userDic)
    userDataList = []
    for key, value in userDic.items():
        userDataList.append({
            'name': key,
            'value': value
        })

    return total_follower_over_10m, max_hot_weibo_likes, xData2, yData2, followerList_list, xData3, yData3, userDataList, xData4, yData4_1, yData4_2, yData4_3


if __name__ == '__main__':
    data = getDaPingData()
    # 输出结果以便调试
    print(data)

