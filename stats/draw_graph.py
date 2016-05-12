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
    plt.ylim(0, max(user_num) + 1000)
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


# 画图主函数
def main():
    verified_draw()
    gender_draw()
    province_draw()

if __name__ == '__main__':
    main()
