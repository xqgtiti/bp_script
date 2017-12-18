# -*- coding:utf-8 -*- -
import os
import shutil
import platform
import sys
import datetime
import shlex, subprocess

from global_path import *
from command import *
from dex_process.single_dex import *
from dex_process.multi_dex import *
from androguard.core.bytecodes import apk

import pypinyin
from pypinyin import lazy_pinyin
from pypinyin import pinyin
reload(sys)
sys.setdefaultencoding('gbk')

def process_apk(apk_name):
    return_code = uncompress(PROGUARD_WORK_SPACE_WIN+apk_name,PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/apk_uncompress')
    if int(return_code) != 0:
        #uncompress fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN+'fail_log//'+apk_name+'.txt','w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S')+'\n'+apk_name+'\n'+'Uncompress APK Fail'+'\n')
        f_fail.close()
        return

    apk_uncompress_path = PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/apk_uncompress'
    list = os.listdir(apk_uncompress_path)
    print list
    class_dex_cnt = 0
    for file in list:
        if 'classes' in file and '.dex' in file:
            class_dex_cnt = class_dex_cnt + 1

    if class_dex_cnt == 1:
        log_info('APK_NAME:'+apk_name+'(%s)'%'single-dex')
        print ('APK_NAME:'+apk_name+'(%s)'%'single-dex')
        single_res = single_dex(apk_name)
        if single_res == 1:
            single_repack(apk_name)
    else:
        log_info('APK_NAME:'+apk_name+'(%s)'%'multi-dex')
        print ('APK_NAME:'+apk_name+'(%s)'%'multi-dex')
        multi_res = multi_dex(apk_name,class_dex_cnt)
        if multi_res == 1:
            multi_repack(apk_name,class_dex_cnt)

def SLOVE():
    list = os.listdir(PROGUARD_WORK_SPACE_WIN)
    #print list
    table = {}
    f = open(PROGUARD_WORK_SPACE_WIN+'success.txt','rb')
    while True:
        r = f.readline()
        if not r: break
        r = r[:-2]
        table[r] = 1


    for ff in list:
        print ff
        if '.apk' in ff and os.path.isdir(PROGUARD_WORK_SPACE_WIN+ff) == False:
            ff_name = ff
            ff_name = ff_name.replace(' ','')
            pinyin_list = lazy_pinyin(u'%s'%ff_name.decode('gbk'))
            ss = ""
            for i in pinyin_list:
                ss = ss+i

            os.chdir(PROGUARD_WORK_SPACE_WIN)
            os.system('rename "%s" %s'%(ff, ss))
            try:
                if table[ss] == 1: continue
            except:
                process_apk(str(ss))

if __name__ == '__main__':
   #process_apk('com.jonathanrobins.pepe_snap.apk')
   SLOVE()

