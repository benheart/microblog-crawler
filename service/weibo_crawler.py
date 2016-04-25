#!/usr/bin/env python
# coding=utf-8

import page_parse
# import random
# import sys
import threading
from utils import pageutil
from dao import dao

# 定义全局变量
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


def get_social_data(user_home_url):
    # 获取用户主页面
    soup = pageutil.get_soup_from_page(user_home_url)
    if soup.title.string == '微博'.decode('utf-8'):
        print '异常账户'
        thread_lock.acquire()
        dao.change_url_status(user_home_url)
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
    soup = pageutil.get_soup_from_page(download_url)
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
        follow_url_list = page_parse.follow_page_parse(user_data_dict, follow_url_list, num)
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        follow_url_list.append(page_parse.follow_page_parse(user_data_dict, follow_url_list, (page_num + 1)))
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
        fans_url_list = page_parse.fans_page_parse(user_data_dict, fans_url_list, num)
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        fans_url_list.append(page_parse.fans_page_parse(user_data_dict, fans_url_list, (page_num + 1)))
    return fans_url_list


def analyze_profile(user_data_dict):
    profile_info_list = []
    profile_total = int(user_data_dict['profile'])
    page_num = profile_total / 10
    page_last = profile_total % 10
    profile_data_dict = {'profile_id': '',
                         'profile_time': '',
                         'profile_source': '',
                         'profile_like': '',
                         'profile_forward': '',
                         'profile_comment': ''}
    for num in xrange(1, page_num + 1):
        result = page_parse.profile_page_parse(user_data_dict, profile_data_dict, profile_info_list, num)
        profile_info_list = result[0]
        if result[2] < 1451577600:
            break
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        result = page_parse.profile_page_parse(user_data_dict, profile_data_dict, profile_info_list, (page_num + 1))
        profile_info_list.append(result[0])
    return profile_info_list


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
    dao.insert_user_data(user_data_dict)
    dao.change_url_status(url_value)
    # insert_new_url(url_list)
    thread_lock.release()


def main():
    url_value_list = dao.get_url_from_database()
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
        url_value_list = dao.get_url_from_database()
        thread_lock.release()
    # 爬取完成，终止程序
    dao.close_crawler_db()
    print 'Done'
    exit(0)

if __name__ == '__main__':
    main()
