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

def single_repack(apk_name):

    #先复制apk到dir目录下
    comand_line = 'copy %s %s'%(PROGUARD_WORK_SPACE_WIN+apk_name, PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'\\')
    os.system(comand_line)
    log_info('...复制apk到dir目录下 ok')

    #删除apk中的classes.dex文件
    return_code = z7_dele(apk_name,'classes.dex')
    if int(return_code) != 0:
        #删除classes.dex文件失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele classes.dex in apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...删除apk中的classes.dex文件 ok')

    #删除apk中的META-INF文件
    return_code = z7_dele(apk_name,'META-INF')
    if int(return_code) != 0:
        #删除classes.dex文件失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele META-INF in apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...删除apk中的META-INF目录 ok')

    #把新的classes.dex文件放入apk中
    return_code = z7_add(apk_name,'classes.dex')
    if int(return_code) != 0:
        #把新的classes.dex文件放入apk中失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Add New classes.dex to apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...把压缩后的classes.dex放入apk中 ok')


    #对新的apk进行签名
    jarsign(apk_name,KEY_NAME,KEY_PASS)
    log_info('...对新的apk进行签名 ok')







