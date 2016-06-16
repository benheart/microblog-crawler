# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import data_count

# 设置字体，防止中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


# 用户认证情况分布图
def verified_draw():
    # 从Mysql获取认证用户数量和非认证用户数量
    verified_num = data_count.verified_user_num()
    unverified_num = data_count.user_num() - verified_num
    # 设定标签
    labels = [u'认证用户', u'非认证用户']
    user_num = [verified_num, unverified_num]
    # 设定画布序号、大小
    plt.figure(1, figsize=(7, 7))
    # 设定饼状图颜色
    colors = ["aqua", "pink"]
    # Pie Plot
    plt.pie(user_num, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False)
    plt.title(u'用户认证情况分布')
    plt.show()


# 用户性别比例分布图
def gender_draw():
    # 从Mysql获取男性用户数量和女性用户数量
    man_num = data_count.user_man_num()
    woman_num = data_count.user_woman_num()
    # 设定标签
    labels = [u'男', u'女']
    user_num = [man_num, woman_num]
    # 设定画布序号、大小
    plt.figure(2, figsize=(7, 7))
    # 设定饼状图颜色
    colors = ["aqua", "pink"]
    # Pie Plot
    plt.pie(user_num, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False)
    plt.title(u'用户性别分布')
    plt.show()


# 用户省份分布图
def province_draw():
    labels = []
    user_num = []
    # 从省份字典中读取数据
    province_dict = data_count.province_num()
    for province in sorted(province_dict.items(), cmp=lambda x, y: cmp(x[1], y[1]), reverse=True):
        labels.append(province[0])
        user_num.append(province[1])
    # 获取数据组数
    n_groups = len(user_num)
    # 设置图像名称、大小
    plt.figure(3, figsize=(16, 8))
    index = np.arange(n_groups)
    # 设置柱宽
    bar_width = 0.5
    # 颜色透明度
    opacity = 0.7
    # 设置柱状的位置、数值、柱宽、颜色透明度、颜色、标签
    plt.bar(index + bar_width, user_num, bar_width, alpha=opacity, color='orange', label=u'省份')
    # 设置x,y轴范围
    plt.ylim(0, max(user_num) + 5000)
    plt.xlim(0, len(user_num) + 0.5)
    # 设置x轴标签以及标签的位置
    plt.xticks(index + bar_width * 1.5, labels)
    # 设置x,y坐标含义、图像标题
    plt.xlabel(u'省份名称')
    plt.ylabel(u'用户数量')
    plt.title(u'用户省份分布')
    plt.legend()
    plt.tight_layout()
    plt.show()


# 用户年龄分布图
def birthday_draw():
    others = 0
    labels = [u'50后', u'60后', u'70后', u'80后', u'90后', u'00后']
    user_num = [0, 0, 0, 0, 0, 0]
    birthday_dict = data_count.birthday_num()
    for birthday in birthday_dict.items():
        if 1950 <= int(birthday[0]) < 1960:
            user_num[0] += birthday[1]
        elif 1960 <= int(birthday[0]) < 1970:
            user_num[1] += birthday[1]
        elif 1970 <= int(birthday[0]) < 1980:
            user_num[2] += birthday[1]
        elif 1980 <= int(birthday[0]) < 1990:
            user_num[3] += birthday[1]
        elif 1990 <= int(birthday[0]) < 2000:
            user_num[4] += birthday[1]
        elif 2000 <= int(birthday[0]) < 2010:
            user_num[5] += birthday[1]
        else:
            others += birthday[1]
    # 打印脏数据条数
    print others
    # 获取数据组数
    n_groups = len(user_num)
    # 设置图像名称、大小
    plt.figure(4, figsize=(8, 5))
    index = np.arange(n_groups)
    # 设置柱宽
    bar_width = 0.5
    # 颜色透明度
    opacity = 0.7
    # 设置柱状的位置、数值、柱宽、颜色透明度、颜色、标签
    plt.bar(index + bar_width, user_num, bar_width, alpha=opacity, color='orange', label=u'年龄段')
    # 设置x,y轴范围
    plt.ylim(0, max(user_num) + 5000)
    plt.xlim(0, len(user_num) + 0.5)
    # 设置x轴标签以及标签的位置
    plt.xticks(index + bar_width * 1.5, labels)
    # 设置x,y坐标含义、图像标题
    plt.xlabel(u'年龄段')
    plt.ylabel(u'用户数量')
    plt.title(u'用户年龄分布')
    plt.legend()
    plt.tight_layout()
    plt.show()


# 微博数量每天趋势图
def profile_day_draw():
    labels = []
    profile_num = []
    user_num = []
    # 从每天微博字典中读取数据
    profile_dict = data_count.profile_day()
    for profile_day in sorted(profile_dict.items(), cmp=lambda x, y: cmp(x, y), reverse=False):
        labels.append(profile_day[0])
        profile_num.append(profile_day[1])
        user_num.append(int(profile_day[0]) - 0.25)
    # 获取数据组数
    n_groups = len(profile_num)
    # 设置图像名称、大小
    plt.figure(5, figsize=(16, 8))
    index = np.arange(n_groups)
    # 设置柱宽
    bar_width = 0.5
    # 颜色透明度
    opacity = 0.7
    # 折线的横纵坐标
    plt.plot(user_num, profile_num, 'bo', user_num, profile_num, 'k')
    # 设置柱状的位置、数值、柱宽、颜色透明度、颜色、标签
    plt.bar(index + bar_width, profile_num, bar_width, alpha=opacity, color='orange', label=u'天')
    # 设置x,y轴范围
    plt.ylim(0, max(profile_num) + 5000)
    plt.xlim(0, len(profile_num) + 0.5)
    # 设置x轴标签以及标签的位置
    plt.xticks(index + bar_width * 1.5, labels)
    # 设置x,y坐标含义、图像标题
    plt.xlabel(u'4月日期')
    plt.ylabel(u'微博数量')
    plt.title(u'4月1-28号微博数量趋势图')
    plt.legend()
    plt.tight_layout()
    plt.show()


# 微博数量每小时趋势图
def profile_hour_draw():
    labels = []
    profile_num = []
    user_num = []
    # 从每小时微博字典中读取数据
    profile_dict = data_count.profile_hour()
    for profile_hour in sorted(profile_dict.items(), cmp=lambda x, y: cmp(x, y), reverse=False):
        labels.append(profile_hour[0])
        profile_num.append(profile_hour[1])
        user_num.append(int(profile_hour[0]) + 0.75)
    # 获取数据组数
    n_groups = len(profile_num)
    # 设置图像名称、大小
    plt.figure(6, figsize=(16, 8))
    index = np.arange(n_groups)
    # 设置柱宽
    bar_width = 0.5
    # 颜色透明度
    opacity = 0.7
    # 折线的横纵坐标
    plt.plot(user_num, profile_num, 'bo', user_num, profile_num, 'k')
    # 设置柱状的位置、数值、柱宽、颜色透明度、颜色、标签
    plt.bar(index + bar_width, profile_num, bar_width, alpha=opacity, color='orange', label=u'小时')
    # 设置x,y轴范围
    plt.ylim(0, max(profile_num) + 5000)
    plt.xlim(0, len(profile_num) + 0.5)
    # 设置x轴标签以及标签的位置
    plt.xticks(index + bar_width * 1.5, labels)
    # 设置x,y坐标含义、图像标题
    plt.xlabel(u'小时')
    plt.ylabel(u'微博数量')
    plt.title(u'每小时微博数量趋势图')
    plt.legend()
    plt.tight_layout()
    plt.show()


# 微博数量每小时趋势图
def profile_source_draw():
    labels = []
    profile_nums = []
    source_dict = data_count.profile_source()
    num = 0
    for item in sorted(source_dict.items(), cmp=lambda x, y: cmp(x[1], y[1]), reverse=True):
        if num > 20:
            break
        labels.append(item[0])
        profile_nums.append(item[1])
        num += 1
    # 设定画布序号、大小
    plt.figure(7, figsize=(8, 8))
    # 设定饼状图颜色
    colors = ["aqua", "pink", 'yellow', 'green']
    # Pie Plot
    plt.pie(profile_nums, colors=colors, labels=labels, autopct='%1.1f%%', pctdistance=0.8, shadow=False)
    plt.title(u'微博来源比例分布')
    plt.show()


# 画图主函数
def main():
    # verified_draw()
    # gender_draw()
    # province_draw()
    birthday_draw()
    # profile_day_draw()
    # profile_hour_draw()
    # profile_source_draw()


if __name__ == '__main__':
    main()
