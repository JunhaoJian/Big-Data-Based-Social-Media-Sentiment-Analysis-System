import pymysql
import requests
import csv
import os
import time
import random

# 数据库连接信息
db_config = {
    'host': 'localhost',  # 数据库地址
    'user': 'root',  # 用户名
    'password': '123456',  # 用户密码
    'database': 'weibo',  # 数据库名称
    'charset': 'utf8mb4'
}

# 连接数据库
connection = pymysql.connect(**db_config)
cursor = connection.cursor()
# 检查并创建数据库
def check_and_create_database(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS weibo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        conn.select_db('weibo')
        print("数据库 'weibo' 已创建或已存在")
    except Exception as e:
        print(f"无法创建数据库: {e}")

# 创建表的 SQL 语句
create_table_query = '''
CREATE TABLE IF NOT EXISTS weibo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    avatar_large TEXT,
    total_format VARCHAR(255),
    like_cnt INT,
    repost_cnt INT,
    comment_cnt INT,
    full_profile_url TEXT,
    attitudes_count INT,
    comments_count INT,
    reposts_count INT,
    region_name VARCHAR(255),
    text_raw TEXT,
    created_at VARCHAR(255),
    h5_url TEXT
)
'''

# 执行创建表的操作
cursor.execute(create_table_query)
connection.commit()

# 创建 CSV 文件夹并写入表头
file_path = 'file/weiborebang.csv'
if not os.path.exists(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'username',  # 用户名
            'avatar_large',  # 头像链接
            'total_format',  # 总转评赞
            'like_cnt',  # 总点赞数
            'repost_cnt',  # 总转发数
            'comment_cnt',  # 总评论数
            'full_profile_url',  # 详情页链接
            'attitudes_count',  # 热榜点赞数
            'comments_count',  # 热榜评论数
            'reposts_count',  # 热榜转发数
            'region_name',  # 发布地区
            'text_raw',  # 微博内容
            'created_at',  # 发布时间
            'h5_url'  # 视频链接
        ])


# 爬取微博热门榜单并插入数据的函数
def fetch_and_store_weibo_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Cookie': 'XSRF-TOKEN=7KMmJjx5xad4_6jpkMwErRZq; SCF=AtZT_x1aZTTwuNPOgrgWjlWeK-pBPEYsmicOTog6r8O5spvD_UkDGeZ2ZXWKUQdyCUOIcINzOyyVpHBCjgXTQQM.; SUB=_2A25KA7cxDeRhGeFM41EW8SbLzzmIHXVpYLb5rDV8PUNbmtAGLXT5kW9NQL0Ga5Hg45Z_HRgxQ8kMohOa43LNApkH; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhTy6cjN2ABN80zl6TPourl5NHD95QNeon0S02RS0BfWs4DqcjqggjLxK-LBoMLBozLxKnLB.qL1KnXPcis; ALF=02_1731155042; _s_tentry=-; Apache=7741808642476.101.1728569750215; SINAGLOBAL=7741808642476.101.1728569750215; ULV=1728569750348:1:1:1:7741808642476.101.1728569750215:; WBPSESS=Y3amNjhmsKfdz1dfBSTBK-DljlrWtt5UVSSOXwX_FN8uQZEfvv_xM7B5ERjWi7hdAENPBLTKgwL6Ol6XDQOwIDt3SSjd86O0AKY432DOTAwN_UUoi0ZgZZlcfSPcZgPvlHdppKTf--ZIpdON5P5_pg==',
        'Referer': 'https://weibo.com/hot/list/1028039999',
        'Accept': 'application/json, text/plain, */*'
    }

    with open(file_path, 'a', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for page in range(1, 520):
            url = f'https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028039999&containerid=102803_ctg1_9999_-_ctg1_9999_home&extparam=discover%7Cnew_feed&max_id={page}&count=10'
            response = requests.get(url, headers=headers)
            data = response.json().get('statuses', [])

            for sight in data:
                user = sight.get('user', {})
                status_total_counter = user.get('status_total_counter', {})
                avatar_large = user.get('avatar_large', '暂无头像')

                name = user.get('screen_name', '未知用户')
                total_format = status_total_counter.get('total_cnt_format', '暂无数据')
                # like_cnt = status_total_counter.get('like_cnt', 0)
                # repost_cnt = status_total_counter.get('repost_cnt', 0)
                # comment_cnt = status_total_counter.get('comment_cnt', 0)
                like_cnt = int(status_total_counter.get('like_cnt', '0').replace(',', ''))
                repost_cnt = int(status_total_counter.get('repost_cnt', '0').replace(',', ''))
                comment_cnt = int(status_total_counter.get('comment_cnt', '0').replace(',', ''))
                print(f"like_cnt: {like_cnt}, type: {type(like_cnt)}")

                profile_url = user.get('profile_url', '暂无链接')
                full_profile_url = f'https://weibo.com{profile_url}' if profile_url != '暂无链接' else '暂无链接'

                attitudes_count = sight.get('attitudes_count', 0)
                comments_count = sight.get('comments_count', 0)
                reposts_count = sight.get('reposts_count', 0)

                region_name = sight.get('region_name', '暂无地区信息')
                text_raw = sight.get('text_raw', '暂无内容')
                created_at = sight.get('created_at', '未知时间')

                # 尝试提取 h5_url
                h5_url = None
                if 'mix_media_info' in sight:
                    mix_media_info = sight['mix_media_info']
                    if 'items' in mix_media_info:
                        items = mix_media_info['items']
                        for item in items:
                            media_info = item.get('media_info', {})
                            if 'h5_url' in media_info:
                                h5_url = media_info['h5_url']
                                break

                if not h5_url and 'page_info' in sight:
                    page_info = sight['page_info']
                    if 'media_info' in page_info:
                        media_info = page_info['media_info']
                        h5_url = media_info.get('h5_url', None)

                if not h5_url:
                    h5_url = '暂无视频'

                print(f'用户名: {name}, 头像链接: {avatar_large}, 总微博数: {total_format}, 点赞数: {like_cnt}, 转发数: {repost_cnt}, 评论数: {comment_cnt}, 详情页链接: {full_profile_url}, 点赞数: {attitudes_count}, 评论数: {comments_count}, 转发数: {reposts_count}, 发布地区: {region_name}, 微博内容: {text_raw}, 发布时间: {created_at}, 视频链接: {h5_url}')

                # 插入数据到数据库
                insert_query = '''
                INSERT INTO weibo (username, avatar_large, total_format, like_cnt, repost_cnt, comment_cnt,
                                   full_profile_url, attitudes_count, comments_count, reposts_count, region_name,
                                   text_raw, created_at, h5_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (name, avatar_large, total_format, like_cnt, repost_cnt, comment_cnt,
                                              full_profile_url, attitudes_count, comments_count, reposts_count,
                                              region_name, text_raw, created_at, h5_url))
                connection.commit()

                # 写入数据到 CSV
                writer.writerow([
                    name, avatar_large, total_format, like_cnt, repost_cnt, comment_cnt, full_profile_url,
                    attitudes_count, comments_count, reposts_count, region_name, text_raw, created_at, h5_url
                ])

            # 加一个随机延时，避免频繁请求
            delay = random.uniform(1, 3)  # 生成 1 到 3 秒之间的随机浮点数
            print(f'延时 {delay:.2f} 秒...')
            time.sleep(delay)


# 调用爬取和存储数据的函数
fetch_and_store_weibo_data()

# 关闭数据库连接
cursor.close()
connection.close()







