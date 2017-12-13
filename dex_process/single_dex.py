# -*- coding:utf-8 -*- -
from command import *

def single_dex(apk_name):
    return_out = dex2jar(apk_name,"")
    if 'Exception' in return_out:
        #dex2jar fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dex2jar Fail' + '\n' + return_out+ '\n')
        f_fail.close()

    #return_out = jar2dex(apk_name,"")
    """
    if 'Exception' in return_out:
        #dex到jar再到dex出错，是dex2jar工具的bug，使用enjarify尝试
        e_return_out = enjarify(apk_name,"")
        if 'Traceback (most recent call last)' in e_return_out:
            gd = 1
    """
    #可行后，把文件删除(dex2jar没问题)
    rm('"'+PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'\classes-dex2jar-jar2dex.dex"')

    return_code = uncompress(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/classes-dex2jar.jar',
                             PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/classes-dex2jar',
                             )
    if int(return_code) != 0:
        # uncompress fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Uncompress jar Fail' + '\n')
        f_fail.close()
        return




