#!/usr/bin/env python
# coding=utf-8
import time
import requests
import MySQLdb
import random
import sys
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
    cookies = ['_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=0h1ZIaTWu_DHQz; SUB=_2A256FBHYDeTxGeNG4lQX9SnJzjWIHXVZ9r-QrDV6PUNbvtAKLWvkkW1LHespqzEDhKK_FFvqoBQJwEHB0L1MrQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWl2w5PECYleQSXim1uJFnV5JpX5KMt; SSOLoginState=1460691336; gsid_CTandWM=4udiCpOz5iJ2JOaNnwFL4oJZn91',
               '_T_WM=70dba9cc1900b9d195872d0d5db0b77c; SUB=_2A256FeWHDeRxGeNG41sX8C7Izz2IHXVZ-YvPrDV6PUJbstBeLWHykW1LHetUrXNuEV9Qw6BncCWfaYlYaN9XCQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5W1.RklowafO6dgkjgK47v5JpX5o2p; SUHB=0S7y4p4nR5kWXX; SSOLoginState=1460770263; gsid_CTandWM=4uHmCpOz56bqqt796KsNmoI9y77',
               '_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=05iq6bhTk3SHvN; SUB=_2A256FZI6DeTxGeNG4lQX9SnJzjWIHXVZ-T5yrDV6PUJbstAKLWfwkW1LHeuaO79Kw2RYDagUMG1QJfsU_9EFaA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWl2w5PECYleQSXim1uJFnV5JpX5o2p; SSOLoginState=1460789866; gsid_CTandWM=4ufzCpOz5ImkTPoE9BphMoJZn91',
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
        'Cookie': cookies[3],
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
        sql = "select * from %s where url_status = 0 limit 10" % table_name
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
    while soup.title.string == '微博'.decode('utf-8'):
        print '异常账户'
        thread_lock.acquire()
        change_url_status(user_home_url)
        user_home_url = get_url_from_database()
        thread_lock.release()
        soup = get_user_page(user_home_url)
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
                insert_new_url(follow.get('href'))
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
                insert_new_url(follow.get('href'))
            # print follow.get('href')


def analyze_fans(user_data_dict):
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
                insert_new_url(fans.get('href'))
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
                insert_new_url(fans.get('href'))
            # print fans.get('href')


def process_url(thread_name, url_value):
    print "%s processing url: %s" % (thread_name, url_value)
    # 获取用户社交信息
    user_data_dict = get_social_data(url_value)
    # 获取用户资料
    user_data_dict = get_user_data(user_data_dict)

    thread_lock.acquire()
    insert_user_data(user_data_dict)
    change_url_status(url_value)
    thread_lock.release()

    # print 'follow list:'
    # # 爬取关注用户
    # analyze_follow(user_data_dict)
    # print 'fans_list:'
    # # 爬取粉丝用户
    # analyze_fans(user_data_dict)


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
