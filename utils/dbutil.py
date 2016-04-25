#!/usr/bin/env python
# coding=utf-8
import MySQLdb


def get_cursor_db():
    return MySQLdb.Connect(host="localhost", user="root", passwd="5179", db="weibo_crawler", charset='utf8')
