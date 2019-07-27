# -*- coding:utf-8 -*-
# @Time    :2019/7/20 14:58
# @Author  :曾格

""""定义DAO基类"""
import pymysql
import configparser
import logging
import os

logger=logging.getLogger(__name__)   # 那个模块调用这个__name__就是对应的模块名

class BaseDao(object):
    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read('D:\Python\Py_Project\myProject\QQ_SIX\config.ini',encoding='utf-8')

        host=self.config['db']['host']
        user=self.config['db']['user']

        # 读取整数port数据
        port = self.config.getint('db','port')
        password=self.config['db']['password']
        database=self.config['db']['database']
        charset = self.config['db']['charset']
        # print("mysql 连接开始了")
        self.conn=pymysql.connect(host=host,
                                  user=user,
                                  port=port,
                                  password=password,
                                  database=database,
                                  charset=charset)
        # print("mysql 连接完成")
    def close(self):
        """"关闭数据库连接"""
        self.conn.close()