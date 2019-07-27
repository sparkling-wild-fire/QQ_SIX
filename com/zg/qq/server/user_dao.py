# -*- coding:utf-8 -*-
# @Time    :2019/7/20 15:14
# @Author  :曾格

""""用户管理"""
from com.zg.qq.server.base_dao import BaseDao

class UserDao(BaseDao):
    def __init__(self):
        super().__init__()

    def findbyid(self,userid):
        """根据用户id查询用户信息"""
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                sql="select user_id,user_pwd,user_name,user_icon " \
                    "from users where user_id=%s"
                cursor.execute(sql,userid)

                # 提取结果集
                row=cursor.fetchone()
                if row is not None:
                    user={}
                    user['user_id']=row[0]
                    user['user_pwd']=row[1]
                    user['user_name']=row[2]
                    user['user_icon']=row[3]
                    return user
        finally:
            self.close()

    def findfriends(self,userid):
        """"根据id查询好友信息"""
        users=[]
        try:
            # 创建游标对象
            with self.conn.cursor() as cursor:
                # 执行sql操作,为什么要取别名，select返回的数据形式是怎么样的
                sql='select user_id,user_pwd,user_name,user_icon from users where user_id in (select user_id2 as user_id from friend where user_id1 = %s) or user_id in (select user_id1 as user_id from friend where user_id2 = %s)'

                cursor.execute(sql,(userid,userid))
                # 提取结果集
                result_set=cursor.fetchall()
                for row in result_set:
                    user={}
                    user['user_id']=row[0]
                    user['user_pwd']=row[1]
                    user['user_name']=row[2]
                    user['user_icon']=row[3]
                    users.append(user)
        finally:
            self.close()
        return users

if __name__=='__main__':
    u=UserDao()
    uc=u.findbyid(1)
    print(uc)
    # import configparser
    # import pymysql
    # config = configparser.ConfigParser()
    # config.read('config.ini', encoding='utf-8')
    #
    # host = config['db']['host']
    # user = config['db']['user']
    #
    # # 读取整数port数据
    # port = config.getint('db', 'port')
    # password = config['db']['password']
    # database = config['db']['database']
    # charset = config['db']['charset']
    #
    # conn = pymysql.connect(host='127.0.0.1',
    #                             user='zgjxf',
    #                             port=3306,
    #                             password='1520',
    #                             database='qq',
    #                             charset='utf8')
    #
    # print(conn)