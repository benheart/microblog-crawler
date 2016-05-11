# coding=utf-8
import logging

# 创建一个logger
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.INFO)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('C:\\logs\\weibo_crawler.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(filename)s %(funcName)s() line:%(lineno)d] - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)


def get_logger():
    # 返回创建的logger
    return logger
