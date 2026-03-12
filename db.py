from pymysql import *

conn = connect(host='localhost', port=3306, user='root', password='123456', database='weibo', charset='utf8mb4')

cursor = conn.cursor()

def querys(sql,params,type = 'no_select'):
    params = tuple(params)
    cursor.execute(sql,params) # 执行sql语句
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'