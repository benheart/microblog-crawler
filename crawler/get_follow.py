#!/usr/bin/env python
# coding=utf-8
import time
import requests
import random
import threading
import json
import codecs
from utils import logutil

logger = logutil.get_logger()
fp = codecs.open('singers_follow', 'wb', encoding='utf-8')
total = 0


class JSONObject:
    def __init__(self, value):
        self.__dict__ = value


# 获取用户资料线程类
class MyThread(threading.Thread):
    def __init__(self, line, thread_name, u_id):
        threading.Thread.__init__(self)
        self.line = line
        self.thread_name = thread_name
        self.u_id = u_id

    def run(self):
        get_follow(self.line, self.thread_name, self.u_id)
        logger.info("Exiting " + self.thread_name)


def get_user_page(param):
    url_value = 'http://m.weibo.cn/page/json?'
    cookies = [
        '_T_WM=d1ffda353c4c42d89a6dbb744820b8ef; ALF=1467709058; SUB=_2A256V5nbDeTxGeVO4lMW8ivPzDuIHXVZuyeTrDV6PUJbktANLUH6kW1gSa3UlYO_0fyvZMaAPvW9OGnyRA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5o2p5NHD95Q0eh.pS0zfe0MNWs4DqcjsIGU3S0zN; SUHB=0S7ShF29t50pZo; SSOLoginState=1465117067; gsid_CTandWM=4uFyCpOz5O9FNcuMU1eujcYix65; M_WEIBOCN_PARAMS=featurecode%3D20000181%26luicode%3D10000011%26lfid%3D1005051646218964%26fid%3D1005051646218964_-_FOLLOWERS%26uicode%3D10000012',
        '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; gsid_CTandWM=4uhja3a71B2In40PqJhJJcYix65; SUB=_2A256MqDxDeRxGeVO4lMW8ivPzDuIHXVZ3MC5rDV6PUJbstAKLUjykW1LHesYUGIz4hUnaxJS_1lKSUIQ1m1epw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5o2p5NHD95Q0eh.pS0zfe0MN; SUHB=0ft519dfWRO-Pl',
        'SUB=_2A256PFXxDeTxGeNG4lYY9ijMyjuIHXVZ33u5rDV6PUJbstAKLWzekW1LHesd7sojU1i0ss4ytXwcjFrVhXFriw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhbR2V8PomNBLO9pRbubrLJ5JpX5o2p5NHD95Qf1h.X1Kqceh2N; SUHB=0ElKOB8-urUe6H; SSOLoginState=1463297441; _T_WM=b75754462a8d5b5f3b35364fca266ced; M_WEIBOCN_PARAMS=uicode%3D20000174; gsid_CTandWM=4uvkCpOz5CYH7uyKUvAQFoJy60h; H5_INDEX=1; H5_INDEX_TITLE=%E4%BC%8F%E5%8F%88%E8%93%9D%E9%85%B1%E7%88%86%E7%B2%92%E7%B2%92',
        '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; SUB=_2A256LRXNDeRxGeVO4lMW8ivPzDuIHXVZ0buFrDV6PUNbvtANLVj4kW1LHeubF_6JrpQZzGFum3V7gYoE4DA8VA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5KMt; SUHB=0BL4eAF-ObD_7A; gsid_CTandWM=4ugaCpOz5wvV6LXbaH7U1cYix65; M_WEIBOCN_PARAMS=fid%3D100803%26uicode%3D10000011']
    # index = random.randint(0, 3)
    # print index
    # 将User-Agent伪装成浏览器
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cookie': cookies[0],
        'Host': 'm.weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    # 发送请求获取响应页面
    json_text = requests.get(url=url_value, params=param, headers=header).content
    return json_text


def analyze_follow(line, u_id, param):
    json_text = get_user_page(param)
    hwj = json.loads(json_text, encoding='utf-8', object_hook=JSONObject)
    if hwj.count is not None:
        fp.write(line + "###" + unicode(u_id) + "###" + json_text)
        fp.write("\n")
    return hwj.count


def get_follow(line, thread_name, u_id):
    global total
    logger.info("%s processing %s u_id: %d" % (thread_name, line, u_id))
    page = 1
    while 1:
        logger.info("%s processing %s page: %d" % (thread_name, line, page))
        containerid = "100505" + unicode(u_id) + "_-_FOLLOWERS"
        param = {
            "containerid": containerid,
            "page": str(page)
        }
        count = analyze_follow(line, u_id, param)
        if count is None:
            break
        page += 1
        total += 1
        # second = random.randint(0, 10)
        # time.sleep(second)


def main():
    global total
    singers = codecs.open('singers', 'rb', encoding='utf-8')
    line_num = 1
    for line in singers:
        if line_num >= 23:
            hwj = json.loads(line, encoding='utf-8', object_hook=JSONObject)
            line = 'Line-' + unicode(line_num)
            # 创建新线程
            for num in xrange(len(hwj.cards[0].card_group)):
                print total
                if line_num == 23 and num >= 8:
                    u_id = hwj.cards[0].card_group[num].user.id
                    name = 'Thread-' + str(num)
                    thread = MyThread(line, name, u_id)
                    thread.start()
                    thread.join()
                if line_num > 23:
                    u_id = hwj.cards[0].card_group[num].user.id
                    name = 'Thread-' + str(num)
                    thread = MyThread(line, name, u_id)
                    thread.start()
                    thread.join()

        line_num += 1


if __name__ == '__main__':
    main()
