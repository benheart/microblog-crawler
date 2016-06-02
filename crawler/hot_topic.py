#!/usr/bin/env python
# coding=utf-8
import time
import requests
import json
import codecs
from utils import logutil

logger = logutil.get_logger()
fp = codecs.open('comments', 'wb', encoding='utf-8')


class JSONObject:
    def __init__(self, value):
        self.__dict__ = value


def get_user_page(url_value, param):
    cookies = ['SUHB=0vJ4HGlwDBKlne; _T_WM=e5908efc59f62dcd44aa8cfe3e287e58; SUB=_2A256PA2jDeRxGeNG41sX8C7Izz2IHXVZ3pPrrDV6PUJbstANLUvEkW1LHettQjSmOg4BEhbUgpOWB30IRVLxww..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5W1.RklowafO6dgkjgK47v5JpX5o2p5NHD95Qf1hn4So57ShBp; gsid_CTandWM=4uKxCpOz5ICSCk5QA0G1XoI9y77',
               '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; gsid_CTandWM=4uhja3a71B2In40PqJhJJcYix65; SUB=_2A256MqDxDeRxGeVO4lMW8ivPzDuIHXVZ3MC5rDV6PUJbstAKLUjykW1LHesYUGIz4hUnaxJS_1lKSUIQ1m1epw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5o2p5NHD95Q0eh.pS0zfe0MN; SUHB=0ft519dfWRO-Pl',
               'SUB=_2A256PFXxDeTxGeNG4lYY9ijMyjuIHXVZ33u5rDV6PUJbstAKLWzekW1LHesd7sojU1i0ss4ytXwcjFrVhXFriw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhbR2V8PomNBLO9pRbubrLJ5JpX5o2p5NHD95Qf1h.X1Kqceh2N; SUHB=0ElKOB8-urUe6H; SSOLoginState=1463297441; _T_WM=b75754462a8d5b5f3b35364fca266ced; M_WEIBOCN_PARAMS=uicode%3D20000174; gsid_CTandWM=4uvkCpOz5CYH7uyKUvAQFoJy60h; H5_INDEX=1; H5_INDEX_TITLE=%E4%BC%8F%E5%8F%88%E8%93%9D%E9%85%B1%E7%88%86%E7%B2%92%E7%B2%92',
               '_T_WM=f63b4d6278c70f86dcbf71778a5d3015; SUB=_2A256LRXNDeRxGeVO4lMW8ivPzDuIHXVZ0buFrDV6PUNbvtANLVj4kW1LHeubF_6JrpQZzGFum3V7gYoE4DA8VA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFfCw2GN3RyY7P2UsKFBk8x5JpX5KMt; SUHB=0BL4eAF-ObD_7A; gsid_CTandWM=4ugaCpOz5wvV6LXbaH7U1cYix65; M_WEIBOCN_PARAMS=fid%3D100803%26uicode%3D10000011']
    # index = random.randint(0, 3)
    # print index
    # 将User-Agent伪装成浏览器
    header = {
        'Host': 'm.weibo.cn',
        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept': 'text/htm'
                  'l,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept - Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept - Encoding': 'gzip, deflate',
        'Cookie': cookies[0],
        'Connection': 'keep-alive'
    }
    # 发送请求获取响应页面
    json_text = requests.get(url=url_value, params=param, headers=header).content
    # # print sys.getsizeof(html) - 21
    # soup = BeautifulSoup(html, "html.parser")
    # # print soup
    # while soup.title.string == '微博广场'.decode('utf-8'):
    #     print soup.title.string
    #     html = requests.get(url, headers=header).content
    #     soup = BeautifulSoup(html, "html.parser")
    return json_text


def analyze_profiles(url_value, param, reposts_total, comments_total, attitudes_total):
    json_text = get_user_page(url_value, param)
    logger.info(json_text)
    hwj = json.loads(json_text, encoding='utf-8', object_hook=JSONObject)
    for num in xrange(len(hwj.cards[0].card_group)):
        blog_time = hwj.cards[0].card_group[num].mblog.created_at
        # print blog_time
        if unicode(blog_time).__len__() == 11:
            blog_time = time.strftime("%Y-", time.localtime()) + unicode(blog_time)
        if unicode(blog_time).__len__() == 8:
            blog_time = time.strftime("%Y-%m-%d", time.localtime()) + unicode(blog_time).replace(u"今天", "")
        if unicode(blog_time).__len__() == 5 or unicode(blog_time).__len__() == 4:
            minutes = int(filter(unicode.isdigit, blog_time))
            blog_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() - (minutes * 60)))
        # print blog_time
        fp.write('%+10s' % blog_time)
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.mid)
        fp.write('\t')
        if hasattr(hwj.cards[0].card_group[num].mblog, 'textLength'):
            fp.write('%+4s' % unicode(hwj.cards[0].card_group[num].mblog.textLength))
            fp.write('\t')
        else:
            fp.write('None')
            fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.source_allowclick))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.source_type))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.user.id))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.user.profile_url)
        fp.write('\t')
        fp.write('%+6s' % str(hwj.cards[0].card_group[num].mblog.user.statuses_count))
        fp.write('\t')
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.user.verified))
        fp.write('\t')
        # fp.write(hwj.cards[0].card_group[num].mblog.user.remark)
        # fp.write('\t')
        fp.write('%+4s' % unicode(hwj.cards[0].card_group[num].mblog.user.verified_type))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.user.gender)
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.user.mbtype))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.user.ismember))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.user.valid))
        fp.write('\t')
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.user.fansNum))
        fp.write('\t')
        reposts_total += hwj.cards[0].card_group[num].mblog.reposts_count
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.reposts_count))
        fp.write('\t')
        comments_total += hwj.cards[0].card_group[num].mblog.comments_count
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.comments_count))
        fp.write('\t')
        attitudes_total += hwj.cards[0].card_group[num].mblog.attitudes_count
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.attitudes_count))
        fp.write('\t')
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.isLongText))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.mlevel))
        fp.write('\t')
        fp.write('%+10s' % unicode(hwj.cards[0].card_group[num].mblog.biz_feature))
        fp.write('\t')
        if hasattr(hwj.cards[0].card_group[num].mblog, 'page_type'):
            fp.write(unicode(hwj.cards[0].card_group[num].mblog.page_type))
            fp.write('\t')
        else:
            fp.write('None')
            fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.hot_weibo_tags))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.text_tag_tips))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.rid)
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.userType))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.mblog_show_union_info))
        fp.write('\t')
        fp.write(unicode(hwj.cards[0].card_group[num].mblog.created_timestamp))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.bid)
        fp.write('\t')
        # fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.like_count))
        # fp.write('\t')
        fp.write('%+5s' % unicode(hwj.cards[0].card_group[num].mblog.attitudes_status))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.user.screen_name)
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.user.description.replace("\n", " "))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.user.verified_reason.replace("\n", " "))
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.source)
        fp.write('\t')
        fp.write(hwj.cards[0].card_group[num].mblog.text)
        fp.write('\n')
    return hwj.next_cursor, reposts_total, comments_total, attitudes_total


def main():
    reposts_total = 0
    comments_total = 0
    attitudes_total = 0
    url_value = 'http://m.weibo.cn/page/pageJson?'
    param = {
        "containerid": "2305301008087b79a77be32ee0e5d4a0b7a07370e13e__timeline__mobile_guide_-_pageapp:23055763d3d983819d66869c27ae8da86cb176",
        "luicode": "10000011",
        "lfid": "1073037b79a77be32ee0e5d4a0b7a07370e13e",
        "v_p": "11",
        "fid": "2305301008087b79a77be32ee0e5d4a0b7a07370e13e__timeline__mobile_guide_-_pageapp:23055763d3d983819d66869c27ae8da86cb176",
    }
    next_cursor_temp, reposts_total, comments_total, attitudes_total = analyze_profiles(url_value, param, reposts_total, comments_total, attitudes_total)
    hwj = json.loads(next_cursor_temp, object_hook=JSONObject)
    next_cursor = "{\"last_since_id\":" + str(hwj.last_since_id) + \
                  ",\"res_type\":" + str(hwj.res_type) + \
                  ",\"next_since_id\":" + str(hwj.next_since_id) + "}"
    page = 1
    logger.info("Page:%d, Next_cursor:%s" % (page, next_cursor))
    while 1:
        param = {
            "containerid": "2305301008087b79a77be32ee0e5d4a0b7a07370e13e__timeline__mobile_guide_-_pageapp:23055763d3d983819d66869c27ae8da86cb176",
            "luicode": "10000011",
            "lfid": "1073037b79a77be32ee0e5d4a0b7a07370e13e",
            "v_p": "11",
            "fid": "2305301008087b79a77be32ee0e5d4a0b7a07370e13e__timeline__mobile_guide_-_pageapp:23055763d3d983819d66869c27ae8da86cb176",
            "next_cursor": next_cursor,
            "page": str(page)}
        next_cursor_temp, reposts_total, comments_total, attitudes_total = analyze_profiles(url_value, param, reposts_total, comments_total, attitudes_total)
        if next_cursor_temp == '':
            break
        hwj = json.loads(next_cursor_temp, object_hook=JSONObject)
        next_cursor = "{\"last_since_id\":" + str(hwj.last_since_id) + \
                      ",\"res_type\":" + str(hwj.res_type) + \
                      ",\"next_since_id\":" + str(hwj.next_since_id) + "}"
        page += 1
        logger.info("Page:%d, Next_cursor:%s" % (page, next_cursor))
        logger.info('reposts_total:%s\tcomments_total:%s\tattitudes_total:%s' % (reposts_total, comments_total, attitudes_total))
    print 'Done'
    exit(0)

if __name__ == '__main__':
    main()
