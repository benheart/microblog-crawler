#!/usr/bin/env python
# coding=utf-8
import requests
import codecs
from utils import logutil

logger = logutil.get_logger()
fp = codecs.open('internet', 'wb', encoding='utf-8')


class JSONObject:
    def __init__(self, value):
        self.__dict__ = value


def get_user_page(url_value, param):
    cookies = ['_T_WM=859de03d0e92201b94d1691e578ad587; SUB=_2A256T2YXDeTxGeNG4lQX9y7Nwj6IHXVZsApfrDV6PUJbstAKLRjjkW1LHeuUQdNPdiDHUzKduAuOEc9GnnwN7Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhBVrHIyWFlrYBZ4BOfMP1z5JpX5o2p5NHD95Qf1h.cSoM7eK.EWs4Dqc_oi--fiKysi-2Xi--fi-88iKn4i--RiKy2i-zNi--fi-z7iKysi--fiKLhiKnci--fiKLhiKnRi--fiKLhiKnRi--fiK.fiKyWi--fiKLhiKnRi--fiKLhiKnRi--fiKnXi-is; SUHB=0jBYrxR6CLLgze; SSOLoginState=1464538695; gsid_CTandWM=4uSTCpOz5vQOo2PyYkPEZoJZA36; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D39%2526q%253D%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%2526t%253D%26fid%3D100103type%253D3%2526q%253D%25E4%25BA%2592%25E8%2581%2594%25E7%25BD%2591%2526isv%253D2%2526specfilter%253D1%2526log_type%253D7%26uicode%3D10000011',
               '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; gsid_CTandWM=4uhja3a71B2In40PqJhJJcYix65; SUB=_2A256MqDxDeRxGeVO4lMW8ivPzDuIHXVZ3MC5rDV6PUJbstAKLUjykW1LHesYUGIz4hUnaxJS_1lKSUIQ1m1epw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5o2p5NHD95Q0eh.pS0zfe0MN; SUHB=0ft519dfWRO-Pl',
               'SUB=_2A256PFXxDeTxGeNG4lYY9ijMyjuIHXVZ33u5rDV6PUJbstAKLWzekW1LHesd7sojU1i0ss4ytXwcjFrVhXFriw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhbR2V8PomNBLO9pRbubrLJ5JpX5o2p5NHD95Qf1h.X1Kqceh2N; SUHB=0ElKOB8-urUe6H; SSOLoginState=1463297441; _T_WM=b75754462a8d5b5f3b35364fca266ced; M_WEIBOCN_PARAMS=uicode%3D20000174; gsid_CTandWM=4uvkCpOz5CYH7uyKUvAQFoJy60h; H5_INDEX=1; H5_INDEX_TITLE=%E4%BC%8F%E5%8F%88%E8%93%9D%E9%85%B1%E7%88%86%E7%B2%92%E7%B2%92',
               '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; SUB=_2A256LRXNDeRxGeVO4lMW8ivPzDuIHXVZ0buFrDV6PUNbvtANLVj4kW1LHeubF_6JrpQZzGFum3V7gYoE4DA8VA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5KMt; SUHB=0BL4eAF-ObD_7A; gsid_CTandWM=4ugaCpOz5wvV6LXbaH7U1cYix65; M_WEIBOCN_PARAMS=fid%3D100803%26uicode%3D10000011']
    # index = random.randint(0, 3)
    # print index
    # 将User-Agent伪装成浏览器
    header = {
        'Host': 'm.weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Cookie': cookies[0],
        'Connection': 'keep-alive'
    }
    # 发送请求获取响应页面
    json_text = requests.get(url=url_value, params=param, headers=header).content
    return json_text


def analyze_singers(url_value, param):
    json_text = get_user_page(url_value, param)
    fp.write(json_text)
    fp.write("\n")


def main():
    page = 1
    url_value = 'http://m.weibo.cn/page/pageJson?'
    while 1:
        logger.info("Processing Page: %d" % page)
        param = {
            "containerid": "100103type%3D3%26q%3D%E4%BA%92%E8%81%94%E7%BD%91%26isv%3D2%26specfilter%3D1%26log_type%3D7",
            "uid": "5896670192",
            "page": str(page)
        }
        analyze_singers(url_value, param)
        page += 1
    print 'Done'
    exit(0)

if __name__ == '__main__':
    main()
