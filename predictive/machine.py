import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from db import querys

# user_ratings = {
#     "admin":{"秦始皇帝陵博物院(兵马俑)":1},
#     "xiaoye":{"秦始皇帝陵博物院(兵马俑)":1,"《长恨歌》演出":2}
# }

def getUser_ratings():
    user_ratings = {}
    userList = list(querys("select * from user",[],'select'))
    historyList = list(querys("select * from history",[],'select'))

    for user in userList:
        userId = user[0]
        userName = user[1]
        for history in historyList:
            weiboId = history[1]
            try:
                existHistory = querys("select id from history where weibo_id = %s and user_id = %s", [weiboId,userId], 'select')[0][0]
                weiboName = querys("select username from weibo where id = %s", [weiboId], 'select')[0][0]
                historyCount = history[3]
                if user_ratings.get(userName,-1)==-1:
                    user_ratings[userName] = {weiboName:historyCount}
                else:
                    user_ratings[userName][weiboName] = historyCount
            except:
                continue
    # print(user_ratings)
    return user_ratings

def user_basee_collaborative_filtering(user_name, user_ratings,top_n=3):
    # 获取莫表用户的数据
    target_user_ratings = user_ratings[user_name]

    # 保存相似度得分
    user_similarity_scores = {}

    # 目标用户转为numpy数组
    target_user_ratings_list = np.array([
        rating for _ ,rating in target_user_ratings.items()
    ])

    # 计算得分相似度
    for user,rating in user_ratings.items():
        if user == user_name:
            continue
        # 将其他用户数据也转为numpy数组
        user_ratings_list = np.array([rating.get(item,0)for item in target_user_ratings])
        # 计算余弦相似度
        similarity_score = cosine_similarity([user_ratings_list],[target_user_ratings_list])[0][0]
        user_similarity_scores[user] = similarity_score
    sorted_similar_user = sorted(user_similarity_scores.items(),key=lambda x:x[1],reverse=True)
    # print(sorted_similar_user)

    # 根据相似度得分，推荐top_n个用户评分过的景点（选择topn个相似用户作为推荐结果）
    recommended_item = set()
    for similar_user,_ in sorted_similar_user[:top_n]:
        recommended_item.update(user_ratings[similar_user].keys())
    # 过滤
    recommended_item = [item for item in recommended_item if item not in target_user_ratings]
    # print(recommended_item)
    # 返回推荐结果
    return recommended_item

if __name__ == '__main__':
    user_name = "admin"
    user_ratings = getUser_ratings()
    user_basee_collaborative_filtering(user_name,user_ratings)


