from db import *

def getData(userId,weiboId):
    hisData = querys('select id from history where user_id = %s and weibo_id = %s',[userId,weiboId],'select')
    if len(hisData):
        querys('update history set count = count + 1 where weibo_id = %s and user_id = %s',[userId,weiboId])
    else:
        querys('insert into history(user_id, weibo_id, count) values(%s, %s, %s)', [userId, weiboId, 1], 'insert')