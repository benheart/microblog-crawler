#!/usr/bin/env python
# encoding=utf-8

import time
import MySQLdb

crawler_db = MySQLdb.Connect(host="localhost", user="root", passwd="5179", db="weibo_crawler", charset='utf8')
cursor = crawler_db.cursor()
url_total = 0
url_finish_total = 0
user_total = 0
verified_user_total = 0
verified_user_finish_total = 0
profile_total = 0

print '\n'
print 'URL Num:'
for index in range(0, 32):
    table_name = 'url_data' + str(index)
    sql = "select count(*) from %s" % table_name
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                url_num = row[0]
                print '%s: %d' % (table_name, url_num)
                url_total += url_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'Finished URL Num:'
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
                print '%s: %d' % (table_name, url_finish_num)
                url_finish_total += url_finish_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'User Num:'
for index in range(0, 32):
    table_name = 'user_data' + str(index)
    sql = "select count(*) from %s" % table_name
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                user_num = row[0]
                print '%s: %d' % (table_name, user_num)
                user_total += user_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'Verified User Num:'
for index in range(0, 32):
    table_name = 'user_data' + str(index)
    sql = "select count(*) from %s where u_verified = 1" % table_name
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                verified_user_num = row[0]
                print '%s: %d' % (table_name, verified_user_num)
                verified_user_total += verified_user_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'Finished Verified User Num:'
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
                print '%s: %d' % (table_name, verified_user_finish_num)
                verified_user_finish_total += verified_user_finish_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'Profile Num:'
for index in range(0, 32):
    table_name = 'profile_data' + str(index)
    sql = "select count(*) from %s" % table_name
    sql = sql.encode('utf-8')
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                profile_num = row[0]
                print '%s: %d' % (table_name, profile_num)
                profile_total += profile_num
    except MySQLdb.Error, error_info:
        print error_info
        crawler_db.rollback()

print '\n'
print 'Summarize: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print 'URL Total Num：%d' % url_total
print 'URL Finished Total Num：%d' % url_finish_total
print 'Unfinished URL Total Num：%d' % (url_total - url_finish_total)
print 'User Total Num: %d' % user_total
print 'Verified User Total Num: %d' % verified_user_total
print 'Verified User Finished Total Num: %d' % verified_user_finish_total
print 'Profile Total Num: %s' % profile_total
