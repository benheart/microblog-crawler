#!/usr/bin/env python
# encoding=utf-8

import time
import MySQLdb

crawler_db = MySQLdb.Connect(host="localhost", user="root", passwd="5179", db="weibo_crawler", charset='utf8')
cursor = crawler_db.cursor()


def url_num():
    # print '\n'
    # print 'URL Num:'
    url_total = 0
    for index in range(0, 32):
        table_name = 'url_data' + str(index)
        sql = "select count(*) from %s" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    url = row[0]
                    # print '%s: %d' % (table_name, url)
                    url_total += url
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return url_total


def finished_url_num():
    # print '\n'
    # print 'Finished URL Num:'
    url_finish_total = 0
    for index in range(0, 32):
        table_name = 'url_data' + str(index)
        sql = "select count(*) from %s where url_status = 1" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    url_finish_num = row[0]
                    # print '%s: %d' % (table_name, url_finish_num)
                    url_finish_total += url_finish_num
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return url_finish_total


def user_num():
    # print '\n'
    # print 'User Num:'
    user_total = 0
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select count(*) from %s" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    user = row[0]
                    # print '%s: %d' % (table_name, user)
                    user_total += user
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return user_total


def province_num():
    # print '\n'
    # print 'Province Num:'
    province_dict = {}
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select u_province, count(*) from %s group by u_province" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    province_name = row[0]
                    province = row[1]
                    if province_name in province_dict.keys():
                        province_dict[province_name] = province_dict[province_name] + province
                    else:
                        province_dict[province_name] = province
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return province_dict


def birthday_num():
    # print '\n'
    # print 'Birthday Num:'
    birthday_dict = {}
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select DATE_FORMAT(u_birthday, '%Y'), count(*) from " + table_name + \
              " group by DATE_FORMAT(u_birthday, '%Y')"
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    birthday_year = row[0]
                    birthday_year_num = row[1]
                    if birthday_year in birthday_dict.keys():
                        birthday_dict[birthday_year] = birthday_dict[birthday_year] + birthday_year_num
                    else:
                        birthday_dict[birthday_year] = birthday_year_num
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return birthday_dict


def user_man_num():
    # print '\n'
    # print 'User Man Num:'
    man_total = 0
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select count(*) from %s where u_gender = 1" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    man_num = row[0]
                    # print '%s: %d' % (table_name, man_num)
                    man_total += man_num
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return man_total


def user_woman_num():
    # print '\n'
    # print 'User Woman Num:'
    woman_total = 0
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select count(*) from %s where u_gender = 0" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    woman_num = row[0]
                    # print '%s: %d' % (table_name, woman_num)
                    woman_total += woman_num
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return woman_total


def verified_user_num():
    # print '\n'
    # print 'Verified User Num:'
    verified_user_total = 0
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select count(*) from %s where u_verified = 1" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    verified_user = row[0]
                    # print '%s: %d' % (table_name, verified_user)
                    verified_user_total += verified_user
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return verified_user_total


def finished_verified_user_num():
    # print '\n'
    # print 'Finished Verified User Num:'
    verified_user_finish_total = 0
    for index in range(0, 32):
        table_name = 'user_data' + str(index)
        sql = "select count(*) from %s where u_verified = 1 and u_status = 1" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    verified_user_finish_num = row[0]
                    # print '%s: %d' % (table_name, verified_user_finish_num)
                    verified_user_finish_total += verified_user_finish_num
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return verified_user_finish_total


def profile_num():
    # print '\n'
    # print 'Profile Num:'
    profile_total = 0
    for index in range(0, 32):
        table_name = 'profile_data' + str(index)
        sql = "select count(*) from %s" % table_name
        sql = sql.encode('utf-8')
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    profile = row[0]
                    # print '%s: %d' % (table_name, profile)
                    profile_total += profile
        except MySQLdb.Error, error_info:
            print error_info
            crawler_db.rollback()
    return profile_total


def main():
    print 'Summarize: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print 'URL Total Num：%d' % url_num()
    print 'URL Finished Total Num：%d' % finished_url_num()
    print 'Unfinished URL Total Num：%d' % (url_num() - finished_url_num())
    print 'User Total Num: %d' % user_num()
    print 'User Man Total Num: %d' % user_man_num()
    print 'User Woman Total Num: %d' % user_woman_num()
    print 'Verified User Total Num: %d' % verified_user_num()
    print 'Verified User Finished Total Num: %d' % finished_verified_user_num()
    print 'Profile Total Num: %s' % profile_num()
    print 'Province Num: '
    for item in province_num().items():
        print item[0] + ':' + str(item[1])
    print 'Birthday Num: '
    for item in birthday_num().items():
        print item[0] + ':' + str(item[1])


if __name__ == '__main__':
    main()
