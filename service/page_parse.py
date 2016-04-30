#!/usr/bin/env python
# coding=utf-8
import time
import re
from utils import base62
from utils import pageutil
from dao import dao


def follow_page_parse(user_data_dict, follow_url_list, num):
    download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/follow?page=' + str(num)
    # print download_url
    soup = pageutil.get_soup_from_page(download_url)
    follow_block = soup.find_all('td', attrs={'valign': 'top'})
    # 逐行处理当前页面关注用户
    for i in range(0, len(follow_block) / 2):
        follow = follow_block[i * 2 + 1].find_all('a')[0]
        if dao.url_in_database(follow.get('href')):
            # insert_new_url(follow.get('href'))
            follow_url_list.append(follow.get('href'))
    return follow_url_list


def fans_page_parse(user_data_dict, fans_url_list, num):
    download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/fans?page=' + str(num)
    # print download_url
    soup = pageutil.get_soup_from_page(download_url)
    fans_block = soup.find_all('td', attrs={'valign': 'top'})
    # 逐行处理当前页面粉丝用户
    for i in range(0, len(fans_block) / 2):
        fans = fans_block[i * 2 + 1].find_all('a')[0]
        if dao.url_in_database(fans.get('href')):
            # insert_new_url(fans.get('href'))
            fans_url_list.append(fans.get('href'))
            # print fans.get('href')
    return fans_url_list


def profile_page_parse(user_data_dict, num):
    profile_info_list = []
    download_url = 'http://weibo.cn/' + user_data_dict['user_id'] + '/profile?page=' + str(num)
    print download_url
    soup = pageutil.get_soup_from_page(download_url)
    profile_block = soup.find_all('div', id=re.compile('^M_'))
    if len(profile_block) == 0:
        return [profile_info_list, 1459440001]
    profile_first = profile_block[0]
    profile_last = profile_block[len(profile_block) - 1]
    time_source_first = profile_first.find('span', attrs={'class': 'ct'}).contents[0].encode("utf-8").split(' 来自')[0]
    time_source_last = profile_last.find('span', attrs={'class': 'ct'}).contents[0].encode("utf-8").split(' 来自')[0]
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
    if profile_time_first >= 1459440000 or profile_time_last < 1461859200:
        for profile in profile_block:
            # print profile.find('span', attrs={'class': 'ct'}).contents
            time_source = profile.find('span', attrs={'class': 'ct'}).contents[0].encode("utf-8").split(' 来自')
            if len(profile.find('span', attrs={'class': 'ct'}).contents) == 1:
                if len(time_source) == 2:
                    profile_source = time_source[1]
                else:
                    profile_source = ""
            else:
                profile_source = profile.find('span', attrs={'class': 'ct'}).contents[1].string
            profile_source = profile_source.replace("'", "")
            # print time_source
            if len(time_source[0]) == 16:
                profile_time_temp = '2016年' + time_source[0]
                profile_time = time.strptime(profile_time_temp, '%Y\xe5\xb9\xb4%m\xe6\x9c\x88%d\xe6\x97\xa5 %H:%M')
                profile_time = time.mktime(profile_time)
                if 1459440000 <= profile_time < 1461859200:
                    profile_mid = profile.get('id').split('_')[1]
                    profile_id = base62.mid_to_id(profile_mid)
                    profile_tmp = profile.find_all('div')
                    profile_tmp = profile_tmp[len(profile_tmp) - 1].find_all('a')

                    if len(profile.find('span', attrs={'class': 'ct'}).contents) == 1:
                        profile_like = filter(str.isdigit, profile_tmp[len(profile_tmp) - 4].string.encode("utf-8"))
                        profile_forward = filter(str.isdigit, profile_tmp[len(profile_tmp) - 3].string.encode("utf-8"))
                        profile_comment = filter(str.isdigit, profile_tmp[len(profile_tmp) - 2].string.encode("utf-8"))
                    else:
                        profile_like = filter(str.isdigit, profile_tmp[len(profile_tmp) - 5].string.encode("utf-8"))
                        profile_forward = filter(str.isdigit, profile_tmp[len(profile_tmp) - 4].string.encode("utf-8"))
                        profile_comment = filter(str.isdigit, profile_tmp[len(profile_tmp) - 3].string.encode("utf-8"))

                    profile_data_dict = {'profile_id': str(profile_id),
                                         'profile_uid': user_data_dict['user_id'],
                                         'profile_time': time.strftime('%Y-%m-%d %H:%M:%S',
                                                                       time.localtime(profile_time)),
                                         'profile_source': profile_source, 'profile_like': str(profile_like),
                                         'profile_forward': str(profile_forward),
                                         'profile_comment': str(profile_comment)}
                    print profile_data_dict
                    profile_info_list.append(profile_data_dict)
        return [profile_info_list, profile_time_first]
    return [profile_info_list, profile_time_first]
