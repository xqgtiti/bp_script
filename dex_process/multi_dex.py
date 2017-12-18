# -*- coding:utf-8 -*- -
from command import *
from proguard import *

from global_path import *
def test_dex2jar_usable(apk_name, xh):
    return_out = dex2jar(apk_name, xh)
    #if 'Exception'.upper() in return_out.upper():
    if int(return_out) != 0:
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(
            now.strftime(
                '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Test Dex2jar Fail' + '\n' + return_out + '\n' + 'Dex %s' % xh + '\n')
        f_fail.close()
        return 0
    log_info('...Test 将原始dex%s转成jar ok' % xh)
    print ('...Test 将原始dex%s转成jar ok' % xh)

    return_out = jar2dex(apk_name, 'classes%s-dex2jar.jar'%xh)
    if 'Exception'.upper() in return_out.upper():
        #dex2jar fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Test Jar2dex Fail' + '\n' + return_out+ '\n' + 'Dex %s' % xh + '\n')
        f_fail.close()
        return 0
    log_info('...Test 将jar%s重新转成dex ok' % xh)
    print ('...Test 将jar%s重新转成dex ok' % xh)
    return 1

#把各个jar下的.class进行归并，用于proguard
def merge(apk_name, num):

    # 创建映射文件，后续重新分包时需要
    f_out = open(PROGUARD_WORK_SPACE_WIN +'dir_'+apk_name+'//map_out.txt', 'w')

    #归并的目录
    merge_dir_path_root = PROGUARD_WORK_SPACE_WIN +'dir_'+apk_name+'\\classes_merge\\'

    if os.path.exists(merge_dir_path_root) == False:
        os.makedirs(merge_dir_path_root)

    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)

        jar_dir_path = PROGUARD_WORK_SPACE_WIN +'dir_'+apk_name+'\\classes%s-dex2jar'%num_s

        #先新建一个文件夹，用于之后划分，然后直接建好里面的目录
        split_dir_path = PROGUARD_WORK_SPACE_WIN +'dir_'+apk_name+'\\classes%s-split\\'%num_s
        if os.path.exists(split_dir_path) == False: os.makedirs(split_dir_path)

        for root, dirs, files in os.walk(jar_dir_path,'rb'):
            for dir in dirs:
                dir_inside = str(os.path.join(root[len(jar_dir_path ) + 1:], dir))
                merge_dir_path = merge_dir_path_root + dir_inside
                if os.path.exists(merge_dir_path) == False:
                    os.makedirs(merge_dir_path)
                if os.path.exists(split_dir_path + dir_inside) == False:
                    os.makedirs(split_dir_path + dir_inside)

            for file in files:
                filePath = str(os.path.join(root, file))
                file_inside = str(os.path.join(root[len(jar_dir_path) + 1:], file))
                merge_file_path = merge_dir_path_root + file_inside
                f_out.write(str(i) + '@@' + file_inside + '\n')
                if os.path.exists(merge_file_path) == False:
                    #print 'cp file:' + merge_file_path
                    shutil.copyfile(filePath, merge_file_path)

#progurad得到jar后，再分包
def split(apk_name, num):
    f_map = open(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '//map_out.txt','rb')
    table = {}
    while True:
        r = f_map.readline()
        if not r: break
        r = r[:-2]
        ll = r.split('@@')
        table[ll[1]] = ll[0]
        #break

    for root, dirs, files in os.walk(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge_out', 'rb'):
        for file in files:
            filePath = str(os.path.join(root, file))
            outside_path = PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge_out\\'
            print outside_path
            print filePath
            tmps = filePath[len(outside_path):]
            print tmps
            print '...'
            if table[tmps] == '1': num_s = ""
            else: num_s = table[tmps]

            head_path = PROGUARD_WORK_SPACE_WIN+ 'dir_' + apk_name +'\\classes_merge_out'
            #print head_path
            inside_path = filePath[len(head_path)+1:]
            #print inside_path

            object_file_path = PROGUARD_WORK_SPACE_WIN+ 'dir_' + apk_name +'\\classes%s-split\\'%num_s+inside_path
            #print object_file_path
            if os.path.exists(object_file_path) == False:
                shutil.copyfile(filePath, object_file_path)

def multi_dex(apk_name, num):

    #先测试dex2jar会不会出现Bug
    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)
        return_code = test_dex2jar_usable(apk_name,num_s)
        print return_code
        if return_code == 1:
            #删除反转回来的dex
            os.system('del classes%s-dex2jar-jar2dex.dex'%num_s)
            gd = 1
        else:
            #需要使用enjarify重新转成jar
            gd = 1
            enjarify(apk_name,num_s)
            os.system('del classes%s-dex2jar.jar'%num_s)
            os.system('rename classes%s-enjarify.jar classes%s-dex2jar.jar'%(num_s,num_s))

            return_out = jar2dex(apk_name, 'classes%s-dex2jar.jar' % num_s)
            if 'Exception'.upper() in return_out.upper():
                # dex2jar fail
                f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
                now = datetime.datetime.now()
                f_fail.write(now.strftime(
                    '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Enjarify Jar2dex Fail' + '\n' + return_out + '\n' + 'Dex %s' % num_s + '\n')
                f_fail.close()
                return 0

            log_info('...Enjarify 将jar%s重新转成dex ok' % num_s)
            print ('...Enjarify 将jar%s重新转成dex ok' % num_s)

    #把各个jar解压

    for i in range(1, num+1):
        if i == 1:
            #file_path, save_path
            return_code = uncompress(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/classes-dex2jar.jar',
                       PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '/classes-dex2jar')

        else:
            return_code = uncompress(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '/classes%d-dex2jar.jar'%i,
                       PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '/classes%d-dex2jar'%i)

        if int(return_code) != 0:
            # uncompress fail
            f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
            now = datetime.datetime.now()
            f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Uncompress Jar Fail' + '\n' + 'Dex %d'%i + '\n')
            f_fail.close()
            return 0

        log_info('...将jar%d解压成目录 ok' % i)
        print ('...将jar%d解压成目录 ok' % i)

    merge(apk_name,num)
    log_info('...merge ok')
    print ('...merge ok')

    #打包成jar 然后使用Proguard
    return_code = jar(
        PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge.jar',
        PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge',apk_name
    )
    if return_code != 0:
        # uncompress fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime(
            '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Pack merge To Jar Fail' + '\n')
        f_fail.close()
        return 0

    log_info('...将merge后的目录打包成jar ok' )
    print ('...将merge后的目录打包成jar ok')


    shrink_multi_dex(apk_name)

    return_code = \
        uncompress(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge_out.jar',
                   PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes_merge_out')

    split(apk_name,num)
    log_info('...split ok')
    print ('...split ok')

    #打包成jar
    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)
        return_code = jar(
            PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes%s-split.jar'%num_s,
            PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\classes%s-split\\'%num_s,apk_name
        )
        if return_code != 0:
            # uncompress fail
            f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
            now = datetime.datetime.now()
            f_fail.write(now.strftime(
                '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Re Pack To Jar Fail' + '\n' + 'Dex %s' % num_s + '\n')
            f_fail.close()
            return 0
        log_info('...将划分后的目录打包成jar%s ok' % num_s)
        print ('...将划分后的目录打包成jar%s ok' % num_s)


    #最后再把jar转成dex
    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)

        return_out = jar2dex(apk_name, 'classes%s-split.jar'%num_s)
        if 'Exception'.upper() in return_out.upper():
            # dex2jar fail
            f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
            now = datetime.datetime.now()
            f_fail.write(
                now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Split Jar2dex Fail' + '\n' + return_out + '\n' + 'dex%s'%num_s + '\n')
            f_fail.close()
            return 0
        log_info('...将shrink过的jar%s转成dex%s ok'%(num_s,num_s))
        print ('...将shrink过的jar%s转成dex%s ok'%(num_s,num_s))

    # 把转换后的dex复制到/new_dex/目录下
    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    os.system('mkdir new_dex')
    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)
        os.system('copy classes%s-split-jar2dex.dex %s' % (num_s,
                PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\new_dex\\classes%s.dex'%num_s))
        log_info('...复制到new_dex目录 dex%s ok'%num_s)

    return 1


def multi_repack(apk_name,num):
    # 1. 先复制apk到dir目录下
    comand_line = 'copy %s %s' % (
    PROGUARD_WORK_SPACE_WIN + apk_name, PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\')
    os.system(comand_line)
    log_info('...复制apk到dir目录下 ok')
    print ('...复制apk到dir目录下 ok')

    # 2. 删除apk中的classes.dex文件
    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)

        return_code = z7_dele(apk_name, 'classes%s.dex'%num_s)
        if int(return_code) != 0:
            # 删除classes.dex文件失败
            f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
            now = datetime.datetime.now()
            f_fail.write(now.strftime(
                '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele classes%s.dex in apk Fail(multi dex)'%num_s + '\n')
            f_fail.close()
            return
        log_info('...删除apk中的classes%s.dex文件 ok'%num_s)
        print ('...删除apk中的classes%s.dex文件 ok'%num_s)

    #3. 删除apk中的META-INF文件
    return_code = z7_dele(apk_name,'META-INF')
    if int(return_code) != 0:
        #删除classes.dex文件失败
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Dele META-INF in apk Fail(multi dex)' + '\n')
        f_fail.close()
        return
    log_info('...删除apk中的META-INF目录 ok')
    print ('...删除apk中的META-INF目录 ok')

    # 4. 把新的classes.dex文件放入apk中

    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)

        return_code = z7_add(apk_name, 'classes%s.dex'%num_s)
        if int(return_code) != 0:
            # 把新的classes.dex文件放入apk中失败
            f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
            now = datetime.datetime.now()
            f_fail.write(now.strftime(
                '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Add New classes%s.dex to apk Fail(multi dex)'%num_s + '\n')
            f_fail.close()
            return
        log_info('...把压缩后的classes%s.dex放入apk中 ok'%num_s)
        print ('...把压缩后的classes%s.dex放入apk中 ok'%num_s)

    # 5. 对新的apk进行签名
    jarsign(apk_name, KEY_NAME, KEY_PASS)
    log_info('...对新的apk进行签名 ok')
    print ('...对新的apk进行签名 ok')


    f = open(PROGUARD_WORK_SPACE_WIN+'\\success.txt','a')
    f.write(apk_name+'\n')


