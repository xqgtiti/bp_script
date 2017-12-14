# -*- coding:utf-8 -*- -
import datetime
import time
import logging
import logging.handlers

PROGUARD_WORK_SPACE_WIN = 'F:\PROGUARD_WORK_SPACE\TOTAL_APK_ROOT_GOOGLE\\'
KEY_NAME = 'demo.keystore'
KEY_PASS = 'zhuzhu66'
LOG_FILE = 'F:\PROGUARD_WORK_SPACE\TOTAL_APK_ROOT_GOOGLE//run_log//%s.txt'%time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)  # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

global logger
logger = logging.getLogger('log')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)

def log_info(s):
    global logger
    logger.info(s)
