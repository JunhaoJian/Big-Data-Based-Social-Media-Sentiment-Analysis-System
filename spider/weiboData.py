import pandas as pd
import random

# 读取现有的 CSV 文件
file_path = './file/weiborebangdata.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 定义生成数据的函数
def generate_follower_count():
    # 大部分在200万到500万之间，其他在500万到1000万之间，少部分在1000万以上
    r = random.random()
    if r < 0.7:
        return random.randint(2000000, 5000000)
    elif r < 0.95:
        return random.randint(5000000, 10000000)
    else:
        return random.randint(10000000, 50000000)

def generate_weibo_count():
    # 大部分在150到400之间，其他在400以上
    r = random.random()
    if r < 0.8:
        return random.randint(150, 400)
    else:
        return random.randint(401, 1000)

def generate_hot_weibo_count():
    # 大部分在10到50之间，少部分在50到98之间，少部分为0，极少部分记作99+
    r = random.random()
    if r < 0.6:
        return random.randint(10, 50)
    elif r < 0.85:
        return random.randint(51, 98)
    elif r < 0.95:
        return 0
    else:
        return '99+'

def generate_hot_weibo_likes(follower_count, weibo_count, hot_weibo_count):
    # 根据粉丝数、微博数、热榜微博数生成热榜微博点赞数
    if hot_weibo_count == 0:
        return 0
    elif isinstance(hot_weibo_count, str) and hot_weibo_count == '99+':
        if follower_count > 10000000 and weibo_count > 400:
            return random.randint(10000000, 50000000)
    elif follower_count <= 5000000 and 150 <= weibo_count <= 400 and 10 <= hot_weibo_count <= 50:
        return random.randint(3000000, 6000000)
    elif 5000000 < follower_count <= 10000000 and weibo_count > 400 and 50 <= hot_weibo_count <= 98:
        return random.randint(5000000, 10000000)
    return random.randint(1000000, 3000000)  # 默认情况

# 增加新的列
df['follower_count'] = df.apply(lambda row: generate_follower_count(), axis=1)
df['weibo_count'] = df.apply(lambda row: generate_weibo_count(), axis=1)
df['hot_weibo_count'] = df.apply(lambda row: generate_hot_weibo_count(), axis=1)
df['hot_weibo_likes'] = df.apply(lambda row: generate_hot_weibo_likes(row['follower_count'], row['weibo_count'], row['hot_weibo_count']), axis=1)

# 保存到新的 CSV 文件
output_file_path = './file/weiborebangdata.csv'
df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print("Data successfully saved to weiborebangdata.csv")
