# -*- coding:utf-8 -*- -
import datetime
import time
import logging
import logging.handlers


TEST_APP_PATH = 'C:\Users\\xqg\Desktop\Test_app\\Instagram_v26.0.0.13.86_apkpure.com.apk'
TEST_APP_DIR = 'C:\Users\\xqg\Desktop\Test_app\\'

PROGUARD_WORK_SPACE_WIN = 'G:\PROGUARD_WORK_SPACE\TOTAL_APK_ROOT_GOOGLE\\'
KEY_NAME = 'demo.keystore'
KEY_PASS = 'zhuzhu66'
PROGUARD_LIB_PATH = 'D:\workspace//big_program//tool\proguard5.3.3\lib\proguard.jar'


TOP_100_PATH = 'G:\PROGUARD_WORK_SPACE\TOP100_TEST\\'
GET_TOP_APK_PATH = 'G:\PROGUARD_WORK_SPACE\GET_TOP_APK\\'
APK_SOTRAGE_PATH = 'G:\PROGUARD_WORK_SPACE\GET_TOP_APK\APK_STORAGE\\'

LOG_FILE = 'run_log//%s.txt'%time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'

formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)

global logger
logger = logging.getLogger('log')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def log_info(s):
    global logger
    logger.info(s)
