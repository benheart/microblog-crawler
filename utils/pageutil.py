#!/usr/bin/env python
# coding=utf-8
import requests
from bs4 import BeautifulSoup


# 根据URL获取Html页面，并通过BeautifulSoup处理Html转换成soup对象
def get_soup_from_page(url):
    # cookies数组
    cookies = ['SUHB=0C1SdmxhAuD0GI; _T_WM=ec62d89ca44b0e8798607d97a2952888; SUB=_2A256TF9lDeTxGeNG4lQX9C3KyTyIHXVZz2EtrDV6PUJbstANLRbwkW1LHesr_LNWa0CYGkU51d0Nvy-cKOb3jg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5ZLanpUjsJ9VPINShhQlbX5JpX5o2p5NHD95Qf1h.cSoB0Soz7Ws4DqcjOi--fi-zRiKyhi--NiK.4i-i2i--RiK.ciKnNi--Xi-zRi-i2i--Xi-zRi-i2i--Ni-z0iK.cKsLjdG.t; SSOLoginState=1464348469; gsid_CTandWM=4uj5CpOz5lYzr947bodBVoJZ9a0',
               '_T_WM=859de03d0e92201b94d1691e578ad587; SUB=_2A256TF8LDeTxGeNG4lQX9y7Nwj6IHXVZz2FDrDV6PUJbstAKLRLTkW1LHetE51HjD6tHnXeTCV2ZR0hFjArwaQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBVrHIyWFlrYBZ4BOfMP1z5JpX5o2p5NHD95Qf1h.cSoM7eK.EWs4Dqc_oi--fiKysi-2Xi--fi-88iKn4i--RiKy2i-zNi--fi-z7iKysi--fiKLhiKnci--fiKLhiKnRi--fiKLhiKnRi--fiK.fiKyWi--fiKLhiKnRi--fiKLhiKnRi--fiKnXi-is; SUHB=0TPFqPFwUrvamC; SSOLoginState=1464348507',
               '_T_WM=b75754462a8d5b5f3b35364fca266ced; gsid_CTandWM=4uMDCpOz5TGPtUs87KYHqoJZn91; SUB=_2A256TF_XDeTxGeNG4lQX9SnJzjWIHXVZz2GfrDV6PUJbstAKLRGkkW1LHeuVp4TOT81BihiTKbuHaIfnWkfVTg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWl2w5PECYleQSXim1uJFnV5JpX5o2p5NHD95Qf1h.cSo-NSK-4Ws4Dqc_zi--ci-2piK.7i--fiKnci-zNi--Xi-z4iKyFi--ci-zXiK.Ni--ci-i8i-2pi--Ri-i2i-8hi--fiKLhiKnRi--fiKLhiKnR; SUHB=0xnSp_b7VngYRF; SSOLoginState=1464348551',
               'SUHB=0d4OvHaN_XbzND; _T_WM=e5908efc59f62dcd44aa8cfe3e287e58; SUB=_2A256TvrZDeRxGeNG41sX8C7Izz2IHXVZsIaRrDV6PUNbvtBeLU78kW1LHespnLUaHb3-bfRziEw3kmn8NZpUlQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5W1.RklowafO6dgkjgK47v5JpX5KMhUgL.Fo-R1h.ceh5XSh22dJLoI7_rUPLf9PULdriLdntt; SSOLoginState=1464502921; gsid_CTandWM=4uhPCpOz55kCd8ddUVGx5oI9y77',
               '_T_WM=0df70571141fd14c4894455bbf56cf38; SUHB=0IIFj-WzktDX9m; SUB=_2A256TF-cDeTxGeVK6lIZ9ifKyDyIHXVZz2HUrDV6PUJbstAKLVXjkW1LHeuTNq0w8V23XWVrgkPW6ISW8pjIfQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWnXoUopTNdHQSvkKJZR8.R5JpX5o2p5NHD95Q0Sh271hq4Soe7Ws4Dqcj.i--ci-ihi-8Fi--Ri-zNi-8si--Xi-z4iKyFi--RiKnRiKLs; SSOLoginState=1464348620',
               '']
    # index = random.randint(0, 3)
    # 填充请求头
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
    soup = BeautifulSoup(html, "html.parser")
    # 如果跳转到微博广场，重复请求直到获取到想要的页面
    while soup.title.string == '微博广场'.decode('utf-8'):
        print soup.title.string
        html = requests.get(url, headers=header).content
        soup = BeautifulSoup(html, "html.parser")
    return soup
