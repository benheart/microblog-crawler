#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup


# 根据URL获取Html页面，并通过BeautifulSoup处理Html转换成soup对象
def get_soup_from_page(url):
    # cookies数组
    cookies = ['SUHB=0C1SdmxhAueKGe; _T_WM=f04fd2124d7207752ac7e031e81f2b0a; SUB=_2A256N5NZDeTxGeNG4lQX9C3KyTyIHXVZ2z0RrDV6PUJbstAKLRfmkW1LHesajY8gxK0zrtPahKU4k3DBLV2C6w..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZLanpUjsJ9VPINShhQlbX5JpX5o2p5NHD95Qf1h.cSoB0Soz7; SSOLoginState=1463018249',
               'SUB=_2A256KHtYDeTxGeNG4lQX9y7Nwj6IHXVZ0wUQrDV6PUJbstAKLUWjkW1LHetZZb6_XAAjRQemLyy1L0IwSR2seg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBVrHIyWFlrYBZ4BOfMP1z5JpX5o2p5NHD95Qf1h.cSoM7eK.E; SUHB=0KAhd6xqZda5aR; SSOLoginState=1462504201; gsid_CTandWM=4uDMCpOz53WmMKo7dDeSioJZA36; _T_WM=859de03d0e92201b94d1691e578ad587',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUB=_2A256KHu4DeTxGeNG4lYY9ijMyjuIHXVZ0wXwrDV6PUJbstANLWajkW1LHessz4gC1LH_7LEWwKhW2lWSlzEuaQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhbR2V8PomNBLO9pRbubrLJ5JpX5o2p5NHD95Qf1h.X1Kqceh2N; SUHB=0D-VuvhLGP3NYg; SSOLoginState=1462504424; gsid_CTandWM=4u9ACpOz5qSARJRsLKXP7oJy60h',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUHB=0qjkC92qy2Y310; SUB=_2A256KHs7DeTxGeVK6lIZ9ifKyDyIHXVZ0wVzrDV6PUJbstAKLUbEkW1LHetxaZkTKy8vQ7AAnreEZX6qvyJCqQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWnXoUopTNdHQSvkKJZR8.R5JpX5o2p5NHD95Q0Sh271hq4Soe7; SSOLoginState=1462504299; gsid_CTandWM=4uh3CpOz5Q4kGzaqaXrAdejk1aa',
               'SUHB=0qjEfDmPO2Y3yU; _T_WM=e5908efc59f62dcd44aa8cfe3e287e58; gsid_CTandWM=4uOSCpOz5By5GdgTQb9ppoKpB1s; SUB=_2A256KE1dDeRxGeNG41sX8C7Izz2IHXVZ01MVrDV6PUJbstANLXfWkW1LHethR2evrRhgL1VOZ5EotkDtEt1JTQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5W1.RklowafO6dgkjgK47v5JpX5o2p5NHD95Qf1hn4So57ShBp; SSOLoginState=1462517005',
               '']
    # index = random.randint(0, 3)
    # 填充请求头
    header = {
        'Host': 'weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Cookie': cookies[4],
        'Connection': 'keep-alive'
    }
    # 发送请求获取响应页面
    html = requests.get(url, headers=header).content
    # print sys.getsizeof(html) - 21
    soup = BeautifulSoup(html, "html.parser")
    # 如果跳转到微博广场，重复请求直到获取到想要的页面
    while soup.title.string == '微博广场'.decode('utf-8'):
        print soup.title.string
        html = requests.get(url, headers=header).content
        soup = BeautifulSoup(html, "html.parser")
    return soup
