from db import querys


def getAllWeibo():
    # 尝试从数据库获取数据
    weiboList = querys('select * from weibo', [], 'select')

    # 如果未获取到数据，返回空列表
    if not weiboList:
        return []

    def map_fn(item):
        item = list(item)


        return item

    # 使用 map 函数转换数据
    weiboList = list(map(map_fn, weiboList))

    # 返回转换后的列表
    return weiboList
def getAllUser():
    userList = querys('select * from user',[],'select')
    return userList

def getHeadData():
    # 获取所有微博数据
    weiboList = getAllWeibo()
    userList = getAllUser()

    def getWeiboStats(weiboList):
        # 统计总的微博数量（id 的总数）
        totalCount = len(weiboList)

        # 初始化字典来存储用户的点赞数、转发数和评论数
        likeCount = {}
        repostCount = {}
        commentCount = {}

        # 遍历 weiboList 以填充上述字典
        for item in weiboList:
            username = item[1]
            like_cnt = item[4]
            repost_cnt = item[5]
            comment_cnt = item[6]

            likeCount[username] = likeCount.get(username, 0) + like_cnt
            repostCount[username] = repostCount.get(username, 0) + repost_cnt
            commentCount[username] = commentCount.get(username, 0) + comment_cnt

        # 找到总点赞数、总转发数和总评论数最多的用户
        maxLikeUser = max(likeCount, key=likeCount.get)
        maxRepostUser = max(repostCount, key=repostCount.get)
        maxCommentUser = max(commentCount, key=commentCount.get)

        return totalCount, maxLikeUser, maxRepostUser, maxCommentUser

    totalCount, maxLikeUser, maxRepostUser, maxCommentUser = getWeiboStats(weiboList)
    return totalCount, maxLikeUser, maxRepostUser, maxCommentUser
