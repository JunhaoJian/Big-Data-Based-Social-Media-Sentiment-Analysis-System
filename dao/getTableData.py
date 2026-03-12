import pandas as pd
from dao.getPublicData import getAllWeibo


def getTableData():
    # 获取所有博主数据
    weiboList = getAllWeibo()

    # 将数据转换为 DataFrame
    df = pd.DataFrame(weiboList, columns=[
        'id', 'username', 'avatar_large', 'total_format', 'like_cnt',
        'repost_cnt', 'comment_cnt', 'full_profile_url', 'attitudes_count',
        'comments_count', 'reposts_counts', 'region_name', 'text_raw', 'created_at', 'h5_url'
    ])

    # 去重处理：只保留第一次出现的 username
    df = df.drop_duplicates(subset='username')

    # 清理 region_name 字段：去除“发布于”字样
    df['region_name'] = df['region_name'].str.replace('发布于', '', regex=False)

    # 重新排号 id
    df.reset_index(drop=True, inplace=True)
    df['id'] = df.index + 1  # 从 1 开始编号

    # 提取所需字段并转换为字典列表
    bozhu_table = []
    for index, row in df.iterrows():
        bozhu_info = {
            'user': row['username'],  # 博主
            'full_profile_url': row['full_profile_url'],  # 详情页链接
            'total_format': row['total_format'],  # 总转评赞
            'like_cnt': row['like_cnt'],  # 总点赞数
            'repost_cnt': row['repost_cnt'],  # 总转发数
            'comment_cnt': row['comment_cnt'],  # 总评论数
            'region_name': row['region_name'],  # 发布地区
            'text_raw': row['text_raw'],  # 微博内容
            'h5_url': row['h5_url'],  # 视频链接
            'id': row['id'],  # 编号
        }
        bozhu_table.append(bozhu_info)

    return bozhu_table


if __name__ == '__main__':
    data = getTableData()
    # 输出结果以便调试
    print(data)
