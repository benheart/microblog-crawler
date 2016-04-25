#!/usr/bin/env python
# coding=utf-8
import MySQLdb
from utils import dbutil

WAIT_STATUS = 0
FINISH_STATUS = 1

crawler_db = dbutil.get_cursor_db()
cursor = crawler_db.cursor()


def get_url_from_database():
    url_value_list = []
    for index in range(0, 32):
        table_name = 'url_data' + str(index)
        sql = "select * from %s where url_status = 0 limit 15" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    url_value = row[1]
                    url_value_list.append(url_value)
                return url_value_list
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
            return url_value_list
    return url_value_list


def change_url_status(url_value):
    url_id = hash(url_value)
    table_name = 'url_data' + str(url_id % 32)
    sql = "update %s set url_status = %s where url_id = %s" % (table_name, str(FINISH_STATUS), str(url_id))
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        print 'Change url status successfully! Url_id:' + str(url_id)
    except MySQLdb.Error, error_info:
        print 'Fail to change url status! Url:' + url_value
        print error_info
        crawler_db.rollback()


def insert_new_url(url_value):
    url_id = hash(url_value)
    table_name = 'url_data' + str(url_id % 32)
    sql = "insert into %s (url_id, url_value, url_status) values (%s, '%s', %s)" % \
          (table_name, str(url_id), url_value, str(WAIT_STATUS))
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        print 'Insert url data to the database successfully! Url_id:' + str(url_id)
    except MySQLdb.Error, error_info:
        print 'Fail to insert url data to the database! Url:' + url_value
        print error_info
        crawler_db.rollback()


def url_in_database(url_value):
    url_id = hash(url_value)
    table_name = 'url_data' + str(url_id % 32)
    sql = "select * from %s where url_id = %s" % (table_name, str(url_id))
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            print 'URL: ' + url_value + ' already exist in db!'
            return False
        else:
            return True
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()


def insert_user_data(user_data_dict):
    # 获取用户数据
    u_id = user_data_dict['user_id']
    u_name = user_data_dict['昵称'.decode('utf-8')]
    u_verified = user_data_dict['认证'.decode('utf-8')]
    u_gender = user_data_dict['性别'.decode('utf-8')]
    u_province = user_data_dict['地区'.decode('utf-8')]
    u_birthday = user_data_dict['生日'.decode('utf-8')]
    u_profile_num = user_data_dict['profile']
    u_follow_num = user_data_dict['follow']
    u_fans_num = user_data_dict['fans']
    table_name = 'user_data' + str(int(u_id) % 32)
    # 将用户数据写入数据库
    user_data = (int(u_id), u_name, int(u_verified), int(u_gender), u_province, u_birthday,
                 int(u_profile_num), int(u_follow_num), int(u_fans_num))
    sql = "insert into " + table_name + " (u_id, u_name, u_verified, u_gender, u_province, u_birthday, " \
          "u_profile_num, u_follow_num, u_fans_num) values (%d, '%s', %d, %d, '%s', '%s', %d, %d, %d)" % user_data
    sql = sql.encode('utf-8')
    print sql
    try:
        cursor.execute(sql)
        crawler_db.commit()
        print 'Insert user data to the database successfully! UID:' + u_id
    except MySQLdb.Error, error_info:
        print 'Fail to insert user data to the database! UID:' + u_id
        print error_info
        crawler_db.rollback()


def close_crawler_db():
    crawler_db.close()
