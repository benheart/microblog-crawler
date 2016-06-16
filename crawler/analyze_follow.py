#!/usr/bin/env python
# coding=utf-8
import json
import codecs
from dao import dao

fp = codecs.open('network_singer.csv', 'wb', encoding='utf-8')


class JSONObject:
    def __init__(self, value):
        self.__dict__ = value


def main():
    source_dict = {}
    singers_follow = codecs.open('singers_follow', 'rb', encoding='utf-8')
    line_num = 1
    fp.write("Source,Target,Weight\n")
    for line in singers_follow:
        hwj = line.split('###')
        source, source_fansNum = dao.get_special_user(hwj[1])
        if source not in source_dict.keys():
            source_dict[source] = source_fansNum
    singers_follow = codecs.open('singers_follow', 'rb', encoding='utf-8')
    for line in singers_follow:
        hwj = line.split('###')
        source, source_fansNum = dao.get_special_user(hwj[1])
        follow = json.loads(hwj[2], encoding='unicode', object_hook=JSONObject)
        for index in xrange(len(follow.cards[0].card_group)):
            uid = follow.cards[0].card_group[index].user.id
            screen_name = follow.cards[0].card_group[index].user.screen_name
            statuses_count = follow.cards[0].card_group[index].user.statuses_count
            verified = follow.cards[0].card_group[index].user.verified
            verified_reason = follow.cards[0].card_group[index].user.verified_reason
            description = follow.cards[0].card_group[index].user.description
            verified_type = follow.cards[0].card_group[index].user.verified_type
            gender = follow.cards[0].card_group[index].user.gender
            ismember = follow.cards[0].card_group[index].user.ismember
            fansNum = follow.cards[0].card_group[index].user.fansNum
            if verified is True:
                verified = 1
            else:
                verified = 0
            if gender == 'm':
                gender = 1
            else:
                gender = 0
            if type(fansNum) is unicode:
                fansNum = int(filter(unicode.isdigit, fansNum)) * 10000
            user = {
                'uid': uid,
                'screen_name': screen_name,
                'statuses_count': statuses_count,
                'verified': verified,
                'verified_reason': verified_reason,
                'description': description,
                'verified_type': verified_type,
                'gender': gender,
                'ismember': ismember,
                'fansNum': fansNum
            }
            target = screen_name
            weight = source_fansNum + fansNum
            # dao.insert_special_user(user)
            if target in source_dict.keys() and source != '':
                fp.write("%s,%s,%d\n" % (source, target, weight))
            # if source != '' and target != '':
            #     fp.write("%s,%s,%d\n" % (source, target, weight))
            # exit(0)
        line_num += 1
        # exit(0)


if __name__ == '__main__':
    main()
