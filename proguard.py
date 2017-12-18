# -*- coding:utf-8 -*- -
import sys
import os
import shlex, subprocess

from global_path import *
reload(sys)
sys.setdefaultencoding('utf-8')
def shrink_single_dex(apk_name):

    #把通用的pro文件复制到当前目录
    os.system('copy %s %s'%
              (PROGUARD_WORK_SPACE_WIN+'android_single_dex.pro',
               PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name))

    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    comand_line = 'java -jar "%s" @android_single_dex.pro'%(PROGUARD_LIB_PATH)
    return_code = os.system(comand_line)
    return return_code

def shrink_multi_dex(apk_name):
    # 把通用的pro文件复制到当前目录
    os.system('copy %s %s' %
              (PROGUARD_WORK_SPACE_WIN + 'android_multi_dex.pro',
               PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name))

    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    comand_line = 'java -jar "%s" @android_multi_dex.pro' % (PROGUARD_LIB_PATH)
    return_code = os.system(comand_line)
    return return_code