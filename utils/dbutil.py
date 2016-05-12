#!/usr/bin/env python
# coding=utf-8
import MySQLdb


# 获取Mysql数据库连接
def get_cursor_db():
    return MySQLdb.Connect(host="localhost", user="root", passwd="5179", db="weibo_crawler", charset='utf8')
