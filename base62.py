#!/usr/bin/env python
# coding=utf-8

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def rsplit(s, count):
    f = lambda x: x > 0 and x or 0
    return [s[f(i - count):i] for i in range(len(s), 0, -count)]


def id_to_mid(profile_id):
    result = ''
    for i in rsplit(profile_id, 7):
        str62 = base62_encode(int(i))
        result = str62.zfill(4) + result
    return result.lstrip('0')


def mid_to_id(mid):
    result = ''
    for i in rsplit(mid, 4):
        str10 = str(base62_decode(i)).zfill(7)
        result = str10 + result
    return result.lstrip('0')


def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X
    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num //= base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    str_length = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (str_length - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num
