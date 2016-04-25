#!/usr/bin/env python
# coding=utf-8
import time

import re
import base62
import requests
import MySQLdb
# import random
# import sys
import threading
from bs4 import BeautifulSoup

# 定义全局变量
WAIT_STATUS = 0
FINISH_STATUS = 1
crawler_db = MySQLdb.Connect(host="localhost", user="root", passwd="5179", db="weibo_crawler", charset='utf8')
cursor = crawler_db.cursor()
thread_lock = threading.Lock()


class MyThread(threading.Thread):
    def __init__(self, thread_id, thread_name, url_value):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.url_value = url_value

    def run(self):
        process_url(self.thread_name, self.url_value)
        print "Exiting " + self.thread_name


def get_user_page(url):
    cookies = ['_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=0D-Vuu386P4j2b; SUB=_2A256EfwgDeTxGeNG4lQX9y7Nwj6IHXVZ_YRorDV6PUJbstANLW3kkW1LHet05sdhgjwfNOR0ClMXPnS5SqdvIg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBVrHIyWFlrYBZ4BOfMP1z5JpX5o2p; SSOLoginState=1461030000; gsid_CTandWM=4u60CpOz50N9V4Lc6vwoYoJZA36',
               '_T_WM=70dba9cc1900b9d195872d0d5db0b77c; SUB=_2A256EfuLDeRxGeNG41sX8C7Izz2IHXVZ_YXDrDV6PUJbstAKLUr8kW1LHeuSg7S1a2KqfjtbJZS82riwBndvAw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5W1.RklowafO6dgkjgK47v5JpX5o2p; SUHB=0h15PrOlW_F_k0; SSOLoginState=1461029851; gsid_CTandWM=4ub4CpOz5PNtLVUo5gSD0oI9y77',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUHB=0oU4fzjiURpcpO; gsid_CTandWM=4uOmCpOz5WzFQFpogujlxoKpB1s; SUB=_2A256EC9dDeTxGeNG4loT-C3MwjyIHXVZ-rEVrDV6PUJbstANLUn8kW1LHetNnf9SqvixCVNV_IBD_pQ7Gr6tqQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5aY-EDEL5TiJCLSWnvkWEM5JpX5o2p; SSOLoginState=1460952845',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUHB=0z1QUob9PHGOv-; SUB=_2A256FkKXDeTxGeNG4loT-C3MwjyIHXVZ-W7frDV6PUJbstANLVr-kW1LHesGlTsYDsD7Cbk3hvFA1vxfj1lKaA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5aY-EDEL5TiJCLSWnvkWEM5JpX5o2p; SSOLoginState=1460810439; gsid_CTandWM=4uKQCpOz5KzYeSk8oBfcroKpB1s']
    # index = random.randint(0, 3)
    # print index
    # 将User-Agent伪装成浏览器
    header = {
        'Host': 'weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Cookie': cookies[1],
        'Connection': 'keep-alive'
    }
    # 发送请求获取响应页面
    html = requests.get(url, headers=header).content
    # print sys.getsizeof(html) - 21
    # print html
    soup = BeautifulSoup(html, "html.parser")
    while soup.title.string == '微博广场'.decode('utf-8'):
        print soup.title.string
        html = requests.get(url, headers=header).content
        soup = BeautifulSoup(html, "html.parser")
    return soup


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


def get_social_data(user_home_url):
    # 获取用户主页面
    soup = get_user_page(user_home_url)
    if soup.title.string == '微博'.decode('utf-8'):
        print '异常账户'
        thread_lock.acquire()
        change_url_status(user_home_url)
        thread_lock.release()
        exit(1)
    social_data_block = soup.find('div', attrs={'class': 'tip2'})
    # 新建用户社交信息字典
    user_data_dict = {'user_id': '',
                      'profile': '',
                      'follow': '',
                      'fans': '',
                      '昵称'.decode('utf-8'): '',
                      '认证'.decode('utf-8'): '0',
                      '性别'.decode('utf-8'): '',
                      '地区'.decode('utf-8'): '',
                      '生日'.decode('utf-8'): '0001-00-00'}
    # 找到用户ID、微博数、关注数、粉丝数标签
    user_id = social_data_block.find_all('a')[0].get('href').encode("utf-8")
    user_profile = social_data_block.find('span', attrs={'class': 'tc'}).string.encode("utf-8")
    user_follow = social_data_block.find_all('a')[0].string.encode("utf-8")
    user_fans = social_data_block.find_all('a')[1].string.encode("utf-8")
    # 从字符串中提取数值
    user_data_dict['user_id'] = filter(str.isdigit, user_id)
    user_data_dict['profile'] = filter(str.isdigit, user_profile)
    user_data_dict['follow'] = filter(str.isdigit, user_follow)
    user_data_dict['fans'] = filter(str.isdigit, user_fans)
    return user_data_dict


def get_user_data(user_data_dict):
    download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/info'
    # 获取用户资料页面
    soup = get_user_page(download_url)
    user_data_block = soup.find_all('div', attrs={'class': 'c'})[2]
    length = len(user_data_block.find_all('br'))
    # 提取用户主要资料并写入字典
    for num in range(1, length + 1):
        user_data_tag = user_data_block.contents[(num - 1) * 2].split(':')[0]
        if user_data_tag in user_data_dict:
            user_data_dict[user_data_tag] = user_data_block.contents[(num - 1) * 2].split(':')[1]
    # 如果用户含有认证信息，则将认证标志设置为true
    if user_data_dict['认证'.decode('utf-8')] != '0':
        user_data_dict['认证'.decode('utf-8')] = '1'
    if user_data_dict['性别'.decode('utf-8')] == '男'.decode('utf-8'):
        user_data_dict['性别'.decode('utf-8')] = '1'
    else:
        user_data_dict['性别'.decode('utf-8')] = '0'
    if user_data_dict['地区'.decode('utf-8')] != '':
        user_province = user_data_dict['地区'.decode('utf-8')].split(' ')[0]
        user_data_dict['地区'.decode('utf-8')] = user_province
    if len(user_data_dict['生日'.decode('utf-8')]) != 10:
        user_data_dict['生日'.decode('utf-8')] = '0001-00-00'
    print user_data_dict['昵称'.decode('utf-8')]
    return user_data_dict


def analyze_follow(user_data_dict):
    follow_url_list = []
    # 获取关注总数
    follow_total = int(user_data_dict['follow'])
    # 由于微博只能获取前200关注用户，如果关注数大于200，将关注数设为200
    if follow_total > 200:
        follow_total = 200
    # 计算页面总数page_num，以及最后一页关注数page_last
    page_num = follow_total / 10
    page_last = follow_total % 10
    # 循环每页爬取关注用户
    for num in range(1, page_num + 1):
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/follow?page=' + str(num)
        # print download_url
        soup = get_user_page(download_url)
        follow_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理当前页面关注用户
        for i in range(0, len(follow_block) / 2):
            follow = follow_block[i * 2 + 1].find_all('a')[0]
            if url_in_database(follow.get('href')):
                # insert_new_url(follow.get('href'))
                follow_url_list.append(follow.get('href'))
            # print follow.get('href')
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/follow?page=' + str(page_num + 1)
        # print download_url
        soup = get_user_page(download_url)
        follow_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理最后一页关注用户
        for i in range(0, len(follow_block) / 2):
            follow = follow_block[i * 2 + 1].find_all('a')[0]
            if url_in_database(follow.get('href')):
                # insert_new_url(follow.get('href'))
                follow_url_list.append(follow.get('href'))
            # print follow.get('href')
    return follow_url_list


def analyze_fans(user_data_dict):
    fans_url_list = []
    # 获取粉丝总数
    fans_total = int(user_data_dict['fans'])
    # 由于微博只能获取前200粉丝用户，如果粉丝数大于200，将粉丝数设为200
    if fans_total > 200:
        fans_total = 200
    # 计算页面总数page_num，以及最后一页粉丝数page_last
    page_num = fans_total / 10
    page_last = fans_total % 10
    # 循环每页爬取粉丝用户
    for num in range(1, page_num + 1):
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/fans?page=' + str(num)
        # print download_url
        soup = get_user_page(download_url)
        fans_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理当前页面粉丝用户
        for i in range(0, len(fans_block) / 2):
            fans = fans_block[i * 2 + 1].find_all('a')[0]
            if url_in_database(fans.get('href')):
                # insert_new_url(fans.get('href'))
                fans_url_list.append(fans.get('href'))
            # print fans.get('href')

    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/fans?page=' + str(page_num + 1)
        # print download_url
        soup = get_user_page(download_url)
        fans_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理最后一页粉丝用户
        for i in range(0, len(fans_block) / 2):
            fans = fans_block[i * 2 + 1].find_all('a')[0]
            if url_in_database(fans.get('href')):
                # insert_new_url(fans.get('href'))
                fans_url_list.append(fans.get('href'))
            # print fans.get('href')
    return fans_url_list


def analyze_profile(user_data_dict):
    profile_total = int(user_data_dict['profile'])
    page_num = profile_total / 10
    page_last = profile_total % 10
    for num in xrange(1, page_num + 1):
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/profile?page=' + str(num)
        soup = get_user_page(download_url)
        profile_block = soup.find_all('div', id=re.compile('^M_'))
        profile_first = profile_block[0]
        profile_last = profile_block[len(profile_block) - 1]
        time_source_first = profile_first.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')[0]
        time_source_last = profile_last.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')[0]
        profile_time_first = 0
        profile_time_last = 0
        if len(time_source_first) == 16:
            profile_time_temp = '2016年' + time_source_first
            profile_time_first = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
            profile_time_first = time.mktime(profile_time_first)
        if len(time_source_last) == 16:
            profile_time_temp = '2016年' + time_source_last
            profile_time_last = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
            profile_time_last = time.mktime(profile_time_last)
        if profile_time_first >= 1451577600 or profile_time_last < 1459440000:
            for profile in profile_block:
                time_source = profile.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')
                # print time_source
                if len(time_source[0]) == 16:
                    profile_time_temp = '2016年' + time_source[0]
                    profile_time = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
                    profile_time = time.mktime(profile_time)
                    if 1451577600 <= profile_time < 1459440000:
                        profile_mid = profile.get('id').split('_')[1]
                        profile_id = base62.mid_to_id(profile_mid)
                        profile_tmp = profile.find_all('div')
                        profile_tmp = profile_tmp[len(profile_tmp) - 1].find_all('a')
                        profile_info = []
                        for profile_str in profile_tmp:
                            if profile_str.string is not None:
                                profile_str = profile_str.string.encode("utf-8")
                                if re.search('[0-9]', profile_str) is not None:
                                    num = filter(str.isdigit, profile_str)
                                    profile_info.append(num)
                        profile_like = profile_info[0]
                        profile_forward = profile_info[1]
                        profile_comment = profile_info[2]
                        print 'mid:' + profile_id
                        print '发布时间:' + str(profile_time)
                        print '来源:' + time_source[1]
                        print '点赞数:' + str(profile_like)
                        print '转发数:' + profile_forward
                        print '评论数:' + profile_comment
        if profile_time_first < 1451577600:
            break
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/profile?page=' + str(page_num + 1)
        soup = get_user_page(download_url)
        profile_block = soup.find_all('div', id=re.compile('^M_'))
        profile_first = profile_block[0]
        profile_last = profile_block[len(profile_block) - 1]
        time_source_first = profile_first.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')[0]
        time_source_last = profile_last.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')[0]
        profile_time_first = 0
        profile_time_last = 0
        if len(time_source_first) == 16:
            profile_time_temp = '2016年' + time_source_first
            profile_time_first = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
            profile_time_first = time.mktime(profile_time_first)
        if len(time_source_last) == 16:
            profile_time_temp = '2016年' + time_source_last
            profile_time_last = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
            profile_time_last = time.mktime(profile_time_last)
        if profile_time_first >= 1451577600 or profile_time_last < 1459440000:
            for profile in profile_block:
                time_source = profile.find('span', attrs={'class': 'ct'}).string.encode("utf-8").split(' 来自')
                # print time_source
                if len(time_source[0]) == 16:
                    profile_time_temp = '2016年' + time_source[0]
                    profile_time = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
                    profile_time = time.mktime(profile_time)
                    if 1451577600 <= profile_time < 1459440000:
                        profile_mid = profile.get('id').split('_')[1]
                        profile_id = base62.mid_to_id(profile_mid)
                        profile_tmp = profile.find_all('div')
                        profile_tmp = profile_tmp[len(profile_tmp) - 1].find_all('a')
                        profile_info = []
                        for profile_str in profile_tmp:
                            if profile_str.string is not None:
                                profile_str = profile_str.string.encode("utf-8")
                                if re.search('[0-9]', profile_str) is not None:
                                    num = filter(str.isdigit, profile_str)
                                    profile_info.append(num)
                        profile_like = profile_info[0]
                        profile_forward = profile_info[1]
                        profile_comment = profile_info[2]
                        print 'mid:' + profile_id
                        print '发布时间:' + str(profile_time)
                        print '来源:' + time_source[1]
                        print '点赞数:' + str(profile_like)
                        print '转发数:' + profile_forward
                        print '评论数:' + profile_comment


def process_url(thread_name, url_value):
    print "%s processing url: %s" % (thread_name, url_value)
    # 获取用户社交信息
    user_data_dict = get_social_data(url_value)
    # 获取用户资料
    user_data_dict = get_user_data(user_data_dict)
    # # 爬取关注用户主页URL
    # follow_url_list = analyze_follow(user_data_dict)
    # # 爬取粉丝用户主页URL
    # fans_url_list = analyze_fans(user_data_dict)
    # # 用户主页URL
    # url_list = follow_url_list + fans_url_list
    # 爬取用户微博信息
    # analyze_profile(user_data_dict)

    thread_lock.acquire()
    insert_user_data(user_data_dict)
    change_url_status(url_value)
    # insert_new_url(url_list)
    thread_lock.release()


def main():
    url_value_list = get_url_from_database()
    # 根据URL等待队列循环爬取用户信息
    while len(url_value_list) != 0:
        threads = []
        # 创建新线程
        for num in xrange(len(url_value_list)):
            name = 'Thread-' + str(num)
            thread = MyThread(num, name, url_value_list[num])
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        # time.sleep(random.randint(1, 2))
        thread_lock.acquire()
        url_value_list = get_url_from_database()
        thread_lock.release()
    # 爬取完成，终止程序
    crawler_db.close()
    print 'Done'
    exit(0)

if __name__ == '__main__':
    main()
