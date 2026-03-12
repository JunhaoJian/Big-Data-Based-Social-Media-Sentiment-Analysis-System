from dao.getPublicData import *
from db import querys
import numpy as np
from sklearn.linear_model import LinearRegression

def getYuCe():
    # 获取所有博主数据
    weiboList = getAllWeibo()

    # 使用集合来存储已经处理过的景点名称
    seen_weibo = set()
    names = []
    future_reposts = []
    future_likes = []

    # 遍历景点数据，提取历史数据
    for item in weiboList:
        name = item[1]
        repost = item[5]
        like = item[4]

        # 去重处理
        if name not in seen_weibo:
            seen_weibo.add(name)
            names.append(name)
            future_reposts.append(repost)  # 直接使用当前数据
            future_likes.append(like)  # 直接使用当前数据

    return names, future_reposts, future_likes


# from dao.getPublicData import *
# from db import querys
# import numpy as np
# from sklearn.linear_model import LinearRegression
#
# def getYuCe():
#     # 获取所有景点数据
#     weiboList = getAllWeibo()
#
#     # 初始化字典以存储历史数据
#     historical_data = {}
#
#     # 遍历景点数据，提取历史数据
#     for item in weiboList:
#         name = item[1]  # 景点名称
#         repost = item[8]  # 门票价格
#         like = item[9]  # 销量
#
#         # 去重处理
#         if name not in historical_data:
#             historical_data[name] = {
#                 'reposts': [repost],
#                 'likes': [like]
#             }
#         else:
#             # 仅在价格或销量有变化时更新历史数据
#             if repost not in historical_data[name]['reposts']:
#                 historical_data[name]['reposts'].append(repost)
#             if like not in historical_data[name]['likes']:
#                 historical_data[name]['likes'].append(like)
#
#     # 预测未来一年的数据
#     names = []
#     future_reposts = []
#     future_likes = []
#
#     for name, data in historical_data.items():
#         names.append(name)
#
#         # 检查历史数据长度
#         if len(data['reposts']) < 2 or len(data['likes']) < 2:
#             # 如果数据不足，跳过这个景点
#             continue
#
#         # 假设我们只要最近的数据来进行线性回归
#         model_repost = LinearRegression()
#         model_likes = LinearRegression()
#
#         # 构建训练数据
#         X = np.array(range(len(data['reposts']))).reshape(-1, 1)  # 时间步
#         y_repost = np.array(data['reposts'])
#         y_likes = np.array(data['likes'])
#
#         # 训练模型
#         model_repost.fit(X, y_repost)
#         model_likes.fit(X, y_likes)
#
#         # 预测未来12个月（未来一年的数据）
#         future_X = np.array(range(len(data['reposts']), len(data['reposts']) + 12)).reshape(-1, 1)
#         predicted_reposts = model_repost.predict(future_X)
#         predicted_likes = model_likes.predict(future_X)
#
#         # 将预测结果转为列表
#         future_reposts.append(predicted_reposts.tolist())
#         future_likes.append(predicted_likes.tolist())
#
#     return names, future_reposts, future_likes
