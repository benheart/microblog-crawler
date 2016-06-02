#!/usr/bin/env python
# coding=utf-8
import MySQLdb
from utils import dbutil
from utils import logutil

WAIT_STATUS = 0
FINISH_STATUS = 1
HALF_WAIT_STATUS = 2

# 定义全局Mysql连接、日志logger
crawler_db = dbutil.get_cursor_db()
cursor = crawler_db.cursor()
logger = logutil.get_logger()


# 从Mysql获取URL列表
def get_url_from_database():
    url_value_list = []
    for index in range(0, 32):
        table_name = 'url_data' + str(index)
        sql = "select * from %s where url_status = 0 limit 3" % table_name
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
            logger.error(error_info)
            crawler_db.rollback()
            return url_value_list
    return url_value_list


# 从Mysql获取未爬取的认证用户列表
def get_verified_user():
    verified_user_list = []
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select u_id, u_profile_num from %s where u_status = 0 and u_verified = 1 limit 12" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    user_data_dict = {'user_id': str(row[0]), 'profile': str(row[1])}
                    verified_user_list.append(user_data_dict)
                return verified_user_list
        except MySQLdb.Error, error_info:
            logger.error(error_info)
            crawler_db.rollback()
            return verified_user_list
    return verified_user_list


# 改变URL队列状态
def change_url_status(url_value):
    url_id = hash(url_value)
    table_name = 'url_data' + str(url_id % 32)
    sql = "update %s set url_status = %s where url_id = %s" % (table_name, str(FINISH_STATUS), str(url_id))
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        logger.info('Change url status successfully! TABLE:%s URL:%s' % (table_name, url_value))
    except MySQLdb.Error, error_info:
        logger.warning('Fail to change url status! TABLE:%s URL:%s' % (table_name, url_value))
        logger.error(error_info)
        crawler_db.rollback()


# 改变Mysql中用户爬取状态信息
def change_user_status(u_id):
    table_name = 'user_data' + str(int(u_id) % 32)
    sql = "update %s set u_status = %s where u_id = %s" % (table_name, str(FINISH_STATUS), u_id)
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        logger.info('Change user status successfully! TABLE:%s UID:%d' % (table_name, u_id))
    except MySQLdb.Error, error_info:
        logger.warning('Fail to change user status! TABLE:%s UID:%d' % (table_name, u_id))
        logger.error(error_info)
        crawler_db.rollback()


# 向Mysql插入新的URL
def insert_new_url(url_list):
    for url_value in url_list:
        if url_in_database(url_value):
            url_id = hash(url_value)
            table_name = 'url_data' + str(url_id % 32)
            sql = "insert into %s (url_id, url_value, url_status) values (%s, '%s', %s)" % \
                  (table_name, str(url_id), url_value, str(WAIT_STATUS))
            sql = sql.encode('utf-8')
            try:
                cursor.execute(sql)
                crawler_db.commit()
                logger.info('Insert url data to the database successfully! TABLE:%s URL:%s' % (table_name, url_value))
            except MySQLdb.Error, error_info:
                logger.warning('Fail to insert url data to the database! TABLE:%s URL:%s' % (table_name, url_value))
                logger.error(error_info)
                crawler_db.rollback()


# 判断Mysql是否存在该URL
def url_in_database(url_value):
    url_id = hash(url_value)
    table_name = 'url_data' + str(url_id % 32)
    sql = "select * from %s where url_id = %s" % (table_name, str(url_id))
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            logger.info("URL:%s already exist in TABLE:%s!" % (url_value, table_name))
            return False
        else:
            return True
    except MySQLdb.Error, error_info:
        logger.error(error_info)
        crawler_db.rollback()


# 向Mysql中插入用户信息
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
    # 将用户数据写入数据库
    table_name = 'user_data' + str(int(u_id) % 32)
    user_data = (int(u_id), u_name, int(u_verified), int(u_gender), u_province, u_birthday,
                 int(u_profile_num), int(u_follow_num), int(u_fans_num))
    sql = "insert into " + table_name + " (u_id, u_name, u_verified, u_gender, u_province, u_birthday, " \
          "u_profile_num, u_follow_num, u_fans_num) values (%d, '%s', %d, %d, '%s', '%s', %d, %d, %d)" % user_data
    logger.info("SQL:" + sql)
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        logger.info('Insert user data to the database successfully! TABLE:%s UID:%s' % (table_name, u_id))
    except MySQLdb.Error, error_info:
        logger.warning('Fail to insert user data to the database! TABLE:%s UID:%s' % (table_name, u_id))
        logger.error(error_info)
        crawler_db.rollback()


# 从Mysql获取未爬取的认证用户列表
def get_special_user(uid):
    screen_name = ''
    fansNum = 0
    sql = "select screen_name, fansNum from user_data where id = " + uid
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                screen_name = row[0]
                fansNum = row[1]
            return screen_name, fansNum
    except MySQLdb.Error, error_info:
        logger.error(error_info)
        crawler_db.rollback()
        return screen_name, fansNum


# 向Mysql中插入特殊用户信息
def insert_special_user(user):
    uid = user['uid']
    screen_name = user['screen_name'].replace("'", "")
    statuses_count = user['statuses_count']
    verified = user['verified']
    verified_reason = user['verified_reason'].replace("'", "")
    verified_type = user['verified_type']
    gender = user['gender']
    ismember = user['ismember']
    fansNum = user['fansNum']
    user_data = (uid, screen_name, statuses_count, verified, verified_reason,
                 verified_type, gender, ismember, fansNum)
    sql = "insert into user_data (id, screen_name, statuses_count, verified, verified_reason, " \
          "verified_type, gender, ismember, fansNum) values " \
          "(%d, '%s', %d, %d, '%s', %d, %d, %d, %d)" % user_data
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        crawler_db.commit()
        logger.info('Insert user data to the database successfully! UID:%s' % uid)
    except MySQLdb.Error, error_info:
        logger.warning('Fail to insert user data to the database! UID:%s' % uid)
        logger.error(error_info)
        crawler_db.rollback()


# 向Mysql中插入微博信息
def insert_profile_data(profile_info_list):
    for profile_data_dict in profile_info_list:
        profile_id = profile_data_dict['profile_id']
        profile_uid = profile_data_dict['profile_uid']
        profile_time = profile_data_dict['profile_time']
        profile_source = profile_data_dict['profile_source']
        profile_like = profile_data_dict['profile_like']
        profile_forward = profile_data_dict['profile_forward']
        profile_comment = profile_data_dict['profile_comment']
        # 将用户微博信息写入数据库
        table_name = 'profile_data' + str(int(profile_id) % 32)
        profile_data = (int(profile_id), int(profile_uid), profile_time, profile_source,
                        int(profile_like), int(profile_forward), int(profile_comment))
        sql = "insert into " + table_name + " (p_id, p_uid, p_time, p_source, p_like, p_forward, p_comment)" \
                                            " values (%d, %d, '%s', '%s', %d, %d, %d)" % profile_data
        logger.info("SQL:" + sql)
        # sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            crawler_db.commit()
            logger.info('Insert profile data to the database successfully! TABLE:%s MID:%s' % (table_name, profile_id))
        except MySQLdb.Error, error_info:
            logger.warning('Fail to insert profile data to the database! TABLE:%s MID:%s' % (table_name, profile_id))
            logger.error(error_info)
            crawler_db.rollback()


# 关闭Mysql数据库连接
def close_crawler_db():
    crawler_db.close()
