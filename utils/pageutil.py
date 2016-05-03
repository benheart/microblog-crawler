#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup


def get_soup_from_page(url):
    cookies = ['SUHB=0YhB9PJa8g9D5o; _T_WM=2c5076056c7618df0a9e39e87f6a597b; gsid_CTandWM=4uhJCpOz5pqzezLIIKQD8oKpB1s; SUB=_2A256IMcXDeTxGeNG4loT-C3MwjyIHXVZ6ulfrDV6PUJbstAKLUajkW1LHes4kxPjmtsKp3m4BtGVGWZF-0X1oA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5aY-EDEL5TiJCLSWnvkWEM5JpX5o2p; SSOLoginState=1462024007',
               '_T_WM=93d448cea0c92fcbc8b7201790ab9213; SUHB=0h15PrOlW_H-Ss; SUB=_2A256IG_2DeRxGeNG41sX8C7Izz2IHXVZ63G-rDV6PUJbrdBeLWr5kW1LHetQ9YY_4RNTeT7MSUMpwxWcsi1PRQ..; gsid_CTandWM=4ulBCpOz5gpWKBhVekuVQoI9y77',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUHB=0OM0LThy-OKkqg; SUB=_2A256IBSNDeTxGeVK6lIZ9ifKyDyIHXVZ6rzFrDV6PUJbstBeLUHbkW1LHet6nK0npR6IqMP_Vz3JlzBpdx65jg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWnXoUopTNdHQSvkKJZR8.R5JpX5o2p; SSOLoginState=1462002909',
               '_T_WM=87c4880b888b3cc3de9172dcb377c48e; SUHB=0nl-btWBYkMmpX; SUB=_2A256INSVDeTxGeVK6lIZ9ifKyDyIHXVZ6vzdrDV6PUNbvtBeLVj1kW1LHet7tzGRpJnD1AguD4JxqK49noPnfw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWnXoUopTNdHQSvkKJZR8.R5JpX5KMt; SSOLoginState=1462019269; gsid_CTandWM=4ujhCpOz5hQslaYExXbRiejk1aa']
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
