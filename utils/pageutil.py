#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup


def get_soup_from_page(url):
    cookies = ['_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=0D-Vuu386P1-LF; SUB=_2A256JqR-DeTxGeNG4lQX9y7Nwj6IHXVZ6Mw2rDV6PUJbstBeLVT1kW1LHeuQ9ZtGXttHopsCt44OquoEYnXeSg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBVrHIyWFlrYBZ4BOfMP1z5JpX5o2p; SSOLoginState=1461900334',
               '_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=0h15PrOlW_H-Ss; SUB=_2A256IG_2DeRxGeNG41sX8C7Izz2IHXVZ63G-rDV6PUJbrdBeLWr5kW1LHetQ9YY_4RNTeT7MSUMpwxWcsi1PRQ..; SSOLoginState=1461985190; gsid_CTandWM=4uHRCpOz56xslm7mYjjDMoI9y77; M_WEIBOCN_PARAMS=uicode%3D20000174',
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
    soup = BeautifulSoup(html, "html.parser")
    while soup.title.string == '微博广场'.decode('utf-8'):
        print soup.title.string
        html = requests.get(url, headers=header).content
        soup = BeautifulSoup(html, "html.parser")
    return soup
