# -*- coding:utf-8 -*- -
from command import *
from global_path import *
from proguard import *
def use_enjarify(apk_name):
    a = 1

def single_dex(apk_name):

    #先把解压后在文件夹apk_uncompress下的classes.dex转成jar
    return_out = dex2jar(apk_name,"")
    if 'Exception' in return_out:
        #dex2jar fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dex2jar Fail' + '\n' + return_out+ '\n')
        f_fail.close()
    log_info('...将原始dex转成jar ok')
    print ('...将原始dex转成jar ok')
    #return_out = jar2dex(apk_name,"")
    """
    if 'Exception' in return_out:
        #dex到jar再到dex出错，是dex2jar工具的bug，使用enjarify尝试
        e_return_out = enjarify(apk_name,"")
        if 'Traceback (most recent call last)' in e_return_out:
            gd = 1
    """
    #可行后，把文件删除(dex2jar没问题)
    #rm('"'+PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'\classes-dex2jar-jar2dex.dex"')

    #使用proguard删除jar文件中的多余代码。
    return_code = shrink_single_dex(apk_name)
    if int(return_code) != 0:
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(
            now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Shrink Fail' + '\n')
        f_fail.close()
    log_info('...使用proguard进行shrink ok')
    print ('...使用proguard进行shrink ok')

    #使用jar2dex把shrink后的jar包转成dex文件
    return_out = jar2dex(apk_name,'classes-dex2jar_out.jar')
    if 'Exception' in return_out:
        #dex2jar fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Jar2dex Fail' + '\n' + return_out+ '\n')
        f_fail.close()
    log_info('...将shrink过的jar转成dex ok')
    print ('...将shrink过的jar转成dex ok')

    #把转换后的dex复制到/new_dex/目录下
    os.system('mkdir new_dex')
    os.system('copy classes-dex2jar_out-jar2dex.dex %s'%(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'\\new_dex\\classes.dex'))
    log_info('...复制到new_dex目录 ok')


#对apk内容进行修改，重新签名
def single_repack(apk_name):

    #1. 先复制apk到dir目录下
    comand_line = 'copy %s %s'%(PROGUARD_WORK_SPACE_WIN+apk_name, PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'\\')
    os.system(comand_line)
    log_info('...复制apk到dir目录下 ok')
    print ('...复制apk到dir目录下 ok')

    #2. 删除apk中的classes.dex文件
    return_code = z7_dele(apk_name,'classes.dex')
    if int(return_code) != 0:
        #删除classes.dex文件失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele classes.dex in apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...删除apk中的classes.dex文件 ok')
    print ('...删除apk中的classes.dex文件 ok')

    #3. 删除apk中的META-INF文件
    return_code = z7_dele(apk_name,'META-INF')
    if int(return_code) != 0:
        #删除classes.dex文件失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele META-INF in apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...删除apk中的META-INF目录 ok')
    print ('...删除apk中的META-INF目录 ok')

    #4. 把新的classes.dex文件放入apk中
    return_code = z7_add(apk_name,'classes.dex')
    if int(return_code) != 0:
        #把新的classes.dex文件放入apk中失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Add New classes.dex to apk Fail(single dex)' + '\n')
        f_fail.close()
        return
    log_info('...把压缩后的classes.dex放入apk中 ok')
    print ('...把压缩后的classes.dex放入apk中 ok')


    #5. 对新的apk进行签名
    jarsign(apk_name,KEY_NAME,KEY_PASS)
    log_info('...对新的apk进行签名 ok')
    print ('...对新的apk进行签名 ok')

"""
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
    """






