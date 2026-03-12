from dao.getPublicData import *
from db import querys


def convert_to_float(value):
    """将带单位的字符串转换为浮点数。"""
    if isinstance(value, str):
        value = value.strip()  # 去除前后空格
        if '万' in value:
            return float(value.replace('万', '')) * 10000  # 将单位转换为实际数值
        elif '千' in value:
            return float(value.replace('千', '')) * 1000  # 将单位转换为实际数值
        else:
            return float(value)  # 直接转换
    return float(value)


def getHomeData():
    # 获取所有博主数据
    weiboList = getAllWeibo()

    # 打印获取的数据
    print("Weibo List:", weiboList)

    total_format_data = {}
    weibo_data = []

    for item in weiboList:
        username = item[1]  # username
        total_format = item[3]  # total_format
        like_cnt = item[4]  # like count
        repost_cnt = item[5]  # repost count
        comment_cnt = item[6]  # comment count
        full_profile_url = item[7]  # full profile URL

        # 打印每个 item 的信息
        print(f"Processing item: {item}")

        # 检查 total_format 是否为有效数值并转换
        try:
            total_format_value = convert_to_float(total_format)
            # 如果 username 还没存入字典，或者当前 total_format 更大，则更新字典
            if username not in total_format_data or total_format_value > total_format_data[username]:
                total_format_data[username] = total_format_value
                # 更新 weibo_data
                weibo_data.append({
                    'username': username,
                    'total_format': total_format_value,
                    'like_cnt': like_cnt,
                    'repost_cnt': repost_cnt,
                    'comment_cnt': comment_cnt,
                    'full_profile_url': full_profile_url
                })
        except ValueError:
            print(f"Could not convert total_format to float for username: {username}, value: {total_format}")
            continue

    # 按照 total_format 排序并取前 100 个用户
    sorted_users = sorted(total_format_data.items(), key=lambda x: x[1], reverse=True)[:100]

    # 解压为两个列表 xData1 和 yData1
    yData1 = [user[0] for user in sorted_users]  # username
    xData1 = [user[1] for user in sorted_users]  # total_format

    return xData1, yData1, weibo_data


if __name__ == '__main__':
    xData1, yData1, weibo_data = getHomeData()
    print("X Data 1:", xData1)
    print("Y Data 1:", yData1)
    print("Weibo Data:", weibo_data)


