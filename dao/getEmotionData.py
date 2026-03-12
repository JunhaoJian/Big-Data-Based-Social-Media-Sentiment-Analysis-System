from dao.getPublicData import *
from db import querys

def getEmotion():
    # 获取所有景点数据
    attractionList = getAllAttractions()

    total_comments = sum(
        int(item[12]) for item in attractionList
        if item[12] is not None and item[12] != '' and isinstance(item[12], (int, float, str)) and not isinstance(item[12],tuple)
    )
    print(total_comments)
    total_goodcomments = sum(
        int(item[13]) for item in attractionList
        if
        item[13] is not None and item[13] != '' and isinstance(item[13], (int, float, str)) and not isinstance(item[13],tuple)
    )
    print(total_goodcomments)
    total_neutralcomments = sum(
        int(item[14]) for item in attractionList
        if
        item[14] is not None and item[14] != '' and isinstance(item[14], (int, float, str)) and not isinstance(item[14],tuple)
    )
    print(total_neutralcomments)
    total_badcomments = sum(
        int(item[15]) for item in attractionList
        if
        item[15] is not None and item[15] != '' and isinstance(item[15], (int, float, str)) and not isinstance(item[15],tuple)
    )
    print(total_badcomments)



