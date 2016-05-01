# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import data_count

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def verified_draw():
    verified_num = data_count.verified_user_num()
    unverified_num = data_count.user_num() - verified_num
    labels = [u'认证用户', u'非认证用户']
    user_num = [verified_num, unverified_num]
    # make a square figure
    plt.figure(1, figsize=(7, 7))
    # Colors used. Recycle if not enough.
    colors = ["aqua", "pink"]
    # Pie Plot
    plt.pie(user_num, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False)
    plt.title(u'用户认证情况分布')
    plt.show()


def gender_draw():
    man_num = data_count.user_man_num()
    woman_num = data_count.user_woman_num()
    labels = [u'男', u'女']
    user_num = [man_num, woman_num]
    # make a square figure
    plt.figure(2, figsize=(7, 7))
    # Colors used. Recycle if not enough.
    colors = ["aqua", "pink"]
    # Pie Plot
    plt.pie(user_num, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False)
    plt.title(u'用户性别分布')
    plt.show()


def province_draw():
    labels = []
    user_num = []
    # Read data
    province_dict = data_count.province_num()
    for province in sorted(province_dict.items(), cmp=lambda x, y: cmp(x[1], y[1]), reverse=True):
        labels.append(province[0])
        user_num.append(province[1])

    n_groups = len(user_num)

    plt.figure(3, figsize=(16, 8))
    index = np.arange(n_groups)
    bar_width = 0.5
    opacity = 0.7
    plt.bar(index + bar_width/2, user_num, bar_width, alpha=opacity, color='orange', label='province')
    plt.xlabel(u'省份名称')
    plt.ylabel(u'用户数量')
    plt.title(u'用户省份分布')
    plt.xticks(index + bar_width, labels)
    plt.ylim(0, max(user_num) + 1000)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    verified_draw()
    gender_draw()
    province_draw()

if __name__ == '__main__':
    main()
