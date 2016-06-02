#!/usr/bin/env python
# coding=utf-8
import json
import codecs
from dao import dao

fp = codecs.open('network.csv', 'wb', encoding='utf-8')


class JSONObject:
    def __init__(self, value):
        self.__dict__ = value


def main():
    singers = codecs.open('singers', 'rb', encoding='utf-8')
    line_num = 1
    for line in singers:
        singer = json.loads(line, encoding='utf-8', object_hook=JSONObject)
        for index in xrange(len(singer.cards[0].card_group)):
            uid = singer.cards[0].card_group[index].user.id
            screen_name = singer.cards[0].card_group[index].user.screen_name
            statuses_count = singer.cards[0].card_group[index].user.statuses_count
            verified = singer.cards[0].card_group[index].user.verified
            verified_reason = singer.cards[0].card_group[index].user.verified_reason
            description = singer.cards[0].card_group[index].user.description
            verified_type = singer.cards[0].card_group[index].user.verified_type
            gender = singer.cards[0].card_group[index].user.gender
            ismember = singer.cards[0].card_group[index].user.ismember
            fansNum = singer.cards[0].card_group[index].user.fansNum
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
            dao.insert_special_user(user)
            # exit(0)
        line_num += 1
        # exit(0)

if __name__ == '__main__':
    main()
