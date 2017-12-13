# -*- coding:utf-8 -*- -
from command import *

def single_dex(apk_name):
    return_out = dex2jar(apk_name)
    if 'Exception' in return_out:
        #dex2jar fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dex2jar Fail' + '\n' + return_out+ '\n')
        f_fail.close()


    return_out = jar2dex(apk_name)


