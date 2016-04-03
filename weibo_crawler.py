#!/usr/bin/env python
# encoding=utf-8
import json
import Queue
import codecs
import requests
from bs4 import BeautifulSoup


# 定义全局变量
USER_HOME_URL = 'http://weibo.cn/1197161814'
social_data_file = codecs.open('social_data_file.txt', 'a', encoding='utf-8')
user_data_file = codecs.open('user_data_file.txt', 'a', encoding='utf-8')


def get_user_page(url):
    # 将User-Agent伪装成浏览器
    header = {
        'Host': 'weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Referer': 'http://login.sina.com.cn/sso/login.php?url=http%3A%2F%2Fweibo.cn%2F&_rand=1459219492.6027&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.16',
        'Cookie': 'SUHB=0mxkCtKIuWUFzd; _T_WM=da865bfb1f2ca6b5ad338e918b880bd5; SUB=_2A257-_ReDeRxGeNG41sX8C7Izz2IHXVZB5wWrDV6PUJbrdANLUnnkW1LHetpn1b55gVewJXjJjlD2nI1xbGYUw..; gsid_CTandWM=4u6077341jCD12g5Fjco2oI9y77',
        'Connection': 'keep-alive',
        'Cache - Control': 'max-age=0'
    }
    # 发送请求获取响应页面
    html = requests.get(url, headers=header).content
    return html


def get_social_data(user_home_url):
    # 获取用户主页面
    html = get_user_page(user_home_url)
    soup = BeautifulSoup(html, "html.parser")
    social_data_block = soup.find('div', attrs={'class': 'tip2'})
    # 新建用户社交信息字典
    social_data_dict = {'user_id': '-', 'profile': '-', 'follow': '-', 'fans': '-'}
    # 找到用户ID、微博数、关注数、粉丝数标签
    user_id = social_data_block.find_all('a')[0].get('href').encode("utf-8")
    user_profile = social_data_block.find('span', attrs={'class': 'tc'}).string.encode("utf-8")
    user_follow = social_data_block.find_all('a')[0].string.encode("utf-8")
    user_fans = social_data_block.find_all('a')[1].string.encode("utf-8")
    # 从字符串中提取数值
    social_data_dict['user_id'] = filter(str.isdigit, user_id)
    social_data_dict['profile'] = filter(str.isdigit, user_profile)
    social_data_dict['follow'] = filter(str.isdigit, user_follow)
    social_data_dict['fans'] = filter(str.isdigit, user_fans)
    # 追加写入用户社交信息文件
    social_data_file.write(social_data_dict['user_id'] + ' ' +
                           social_data_dict['profile'] + ' ' +
                           social_data_dict['follow'] + ' ' +
                           social_data_dict['fans'] + '\n')
    return social_data_dict


def get_user_data(social_data_dict):
    download_url = 'http://weibo.cn/' + social_data_dict['user_id'] + '/info'
    # 获取用户资料页面
    html = get_user_page(download_url)
    soup = BeautifulSoup(html, "html.parser")
    user_data_block = soup.find_all('div', attrs={'class': 'c'})[2]
    length = len(user_data_block.find_all('br'))
    # 新建用户资料字典
    user_data_dict = {'昵称'.decode('utf-8'): '-',
                      '认证'.decode('utf-8'): '-',
                      '性别'.decode('utf-8'): '-',
                      '地区'.decode('utf-8'): '-',
                      '生日'.decode('utf-8'): '-'}
    # 提取用户主要资料并写入字典
    for num in range(1, length + 1):
        user_data_tag = user_data_block.contents[(num - 1) * 2].split(':')[0]
        if user_data_dict.has_key(user_data_tag):
            user_data_dict[user_data_tag] = user_data_block.contents[(num - 1) * 2].split(':')[1]
    # 如果用户含有认证信息，则将认证标志设置为true
    if user_data_dict['认证'.decode('utf-8')] != '-':
        user_data_dict['认证'.decode('utf-8')] = 'true'
    print user_data_dict['昵称'.decode('utf-8')]
    # 追加写入用户资料文件
    user_data_file.write(social_data_dict['user_id'] + ' ' +
                         user_data_dict['昵称'.decode('utf-8')] + ' ' +
                         user_data_dict['认证'.decode('utf-8')] + ' ' +
                         user_data_dict['性别'.decode('utf-8')] + ' ' +
                         user_data_dict['地区'.decode('utf-8')] + ' ' +
                         user_data_dict['生日'.decode('utf-8')] + '\n')


def analyze_follow(social_data_dict):
    # 获取关注总数
    follow_total = int(social_data_dict['follow'])
    # 由于微博只能获取前200关注用户，如果关注数大于200，将关注数设为200
    if follow_total > 200:
        follow_total = 200
    # 计算页面总数page_num，以及最后一页关注数page_last
    page_num = follow_total / 10
    page_last = follow_total % 10
    # 循环每页爬取关注用户
    for num in range(1, page_num + 1):
        download_url = 'http://weibo.cn/' + social_data_dict['user_id'] + '/follow?page=' + str(num)
        print download_url
        html = get_user_page(download_url)
        soup = BeautifulSoup(html, "html.parser")
        follow_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理当前页面关注用户
        for i in range(0, len(follow_block) / 2):
            follow = follow_block[i * 2 + 1].find_all('a')[0]
            print follow
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        download_url = 'http://weibo.cn/' + social_data_dict['user_id'] + '/follow?page=' + str(page_num + 1)
        print download_url
        html = get_user_page(download_url)
        soup = BeautifulSoup(html, "html.parser")
        follow_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理最后一页关注用户
        for i in range(0, len(follow_block) / 2):
            follow = follow_block[i * 2 + 1].find_all('a')[0]
            print follow


def analyze_fans(social_data_dict):
    # 获取粉丝总数
    fans_total = int(social_data_dict['fans'])
    # 由于微博只能获取前200粉丝用户，如果粉丝数大于200，将粉丝数设为200
    if fans_total > 200:
        fans_total = 200
    # 计算页面总数page_num，以及最后一页粉丝数page_last
    page_num = fans_total / 10
    page_last = fans_total % 10
    # 循环每页爬取粉丝用户
    for num in range(1, page_num + 1):
        download_url = 'http://weibo.cn/' + social_data_dict['user_id'] + '/fans?page=' + str(num)
        print download_url
        html = get_user_page(download_url)
        soup = BeautifulSoup(html, "html.parser")
        fans_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理当前页面粉丝用户
        for i in range(0, len(fans_block) / 2):
            fans = fans_block[i * 2 + 1].find_all('a')[0]
            print fans
    # 如果最后一页非空，处理最后一页
    if page_last != 0:
        download_url = 'http://weibo.cn/' + social_data_dict['user_id'] + '/fans?page=' + str(page_num + 1)
        print download_url
        html = get_user_page(download_url)
        soup = BeautifulSoup(html, "html.parser")
        fans_block = soup.find_all('td', attrs={'valign': 'top'})
        # 逐行处理最后一页粉丝用户
        for i in range(0, len(fans_block) / 2):
            fans = fans_block[i * 2 + 1].find_all('a')[0]
            print fans


def close_files():
    social_data_file.close()
    user_data_file.close()


def main():
    # 获取用户社交信息
    social_data_dict = get_social_data(USER_HOME_URL)
    # 获取用户资料
    get_user_data(social_data_dict)
    print 'follow list:'
    # 爬取关注用户
    analyze_follow(social_data_dict)
    print 'fans_list:'
    # 爬取粉丝用户
    analyze_fans(social_data_dict)
    # 关闭文件
    close_files()
    print 'Done'


if __name__ == '__main__':
    main()
