# -*- coding:utf-8 -*- 

"""
@author: xqg
@file: proguard_20180105.py
@time: 2018/1/5 6:57
@desc:

"""
import os
from command import *

ROOT_PATH = 'G:\PROGUARD_WORK_SPACE\TOP100_TEST\\'
REDE_PATH = ROOT_PATH + 'REDE_AND_RESIGIN\\'
PROGUARD_LIB_PATH = 'D:\workspace//big_program//tool\proguard5.3.3\lib\proguard.jar'

def shrink_single_dex(dex_path):

    #把通用的pro文件复制到当前目录
    os.chdir(dex_path)
    if 'enjarify' in dex_path:
        os.system('copy %s %s'%(ROOT_PATH+'android_single_dex_enjarify.pro',dex_path))
        comand_line = 'java -jar "%s" @android_single_dex_enjarify.pro'%(PROGUARD_LIB_PATH)

    elif 'dex2jar' in dex_path:
        os.system('copy %s %s'%(ROOT_PATH+'android_single_dex_dex2jar.pro',dex_path))
        comand_line = 'java -jar "%s" @android_single_dex_dex2jar.pro'%(PROGUARD_LIB_PATH)

    return_code = os.system(comand_line)
    return return_code

def single_dex(dex_path):
    #解压
    shrink_single_dex(dex_path)


#把各个jar下的.class进行归并，用于proguard
def merge(dex_path, num):

    # 创建映射文件，后续重新分包时需要
    f_out = open(dex_path+'map_out.txt', 'w')

    #归并的目录
    merge_dir_path_root = dex_path + 'classes_merge\\'

    if os.path.exists(merge_dir_path_root) == False:
        os.makedirs(merge_dir_path_root)

    for i in range(1, num+1):
        if i == 1: num_s = ""
        else: num_s = str(i)

        if 'dex2jar' in dex_path:
            jar_dir_path = dex_path + 'classes%s-dex2jar'%num_s
        else:
            jar_dir_path = dex_path + 'classes%s-enjarify'%num_s

        #先新建一个文件夹，用于之后划分，然后直接建好里面的目录
        split_dir_path = dex_path + 'classes%s-split\\'%num_s
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
                    try:
                        shutil.copyfile(filePath, merge_file_path)
                    except:
                        os.system('copy %s %s'%(filePath,merge_file_path))

def jar(jar_path, dir_path):
    comand_line = 'jar cvf %s -C %s .'%(jar_path, dir_path)
    print comand_line
    return_code = os.system(comand_line)
    comand_line = '7z d "%s" "%s"' % (jar_path, 'META-INF')
    os.system(comand_line)
    return return_code

def shrink_multi_dex(dex_path):
    # 把通用的pro文件复制到当前目录

    os.system('copy %s %s'%(ROOT_PATH+'android_multi_dex.pro', dex_path))
    os.chdir(dex_path)

    comand_line = 'java -jar "%s" @android_multi_dex.pro'%(PROGUARD_LIB_PATH)
    return_code = os.system(comand_line)
    return return_code

def multi_dex(dex_path, package_path, num):

    if 'dex2jar' in dex_path:
        # 把各个jar解压
        for i in range(1, num + 1):
            if i == 1:
                # file_path, save_path
                return_code = uncompress(dex_path + 'classes-dex2jar.jar',
                                         dex_path + 'classes-dex2jar')

            else:
                return_code = uncompress(dex_path  + 'classes%d-dex2jar.jar' % i,
                                         dex_path + 'classes%d-dex2jar' % i)

            """
            if int(return_code) != 0:
                # uncompress fail
                f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
                now = datetime.datetime.now()
                f_fail.write(now.strftime(
                    '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Uncompress Jar Fail' + '\n' + 'Dex %d' % i + '\n')
                f_fail.close()
                return 0

            log_info('...将jar%d解压成目录 ok' % i)
            print ('...将jar%d解压成目录 ok' % i)
            """

    elif 'enjarify' in dex_path:
        for i in range(1, num + 1):
            if i == 1:
                # file_path, save_path
                return_code = uncompress(dex_path + 'classes-enjarify.jar',
                                         dex_path + 'classes-enjarify')

            else:
                return_code = uncompress(dex_path  + 'classes%d-enjarify.jar' % i,
                                         dex_path + 'classes%d-enjarify' % i)
    #归并
    merge(dex_path=dex_path, num=num )

    # 打包成jar 然后使用Proguard
    return_code = jar(dex_path + 'classes_merge.jar',dex_path + 'classes_merge')

    shrink_multi_dex(dex_path)

    """
    if return_code != 0:
        # uncompress fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN + 'fail_log//' + apk_name + '.txt', 'w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime(
            '%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Pack merge To Jar Fail' + '\n')
        f_fail.close()
        return 0

    log_info('...将merge后的目录打包成jar ok')
    print ('...将merge后的目录打包成jar ok')

    shrink_multi_dex(apk_name)
    """

def slove():
    have_table = {}

    package_list = []
    f_p = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//after_pro.txt','rb')
    while True:
        r = f_p.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        have_table[r] = 1
    f_p.close()

    f_package = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_final.txt', 'rb')
    while True:
        r = f_package.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        package_list.append(r)

    for i in range(33, 34):
        print '#!!! %s'%package_list[i]
        try:
            if have_table[package_list[i]] == 1: continue
        except: gd = 1

        path = REDE_PATH+package_list[i]+'\\'
        f_res = open(path+'process_results.txt')
        r = f_res.readline()
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        inside_list = os.listdir(path)
        apk_name = ""
        dex_path = ""
        if res['dex2jar'] == 1:
            for name in inside_list:
                if name[-4:] == '.apk' and 'dex2jar' in name:
                    apk_name = name
                    dex_path = path + 'dex2jar\\'
        else:
            for name in inside_list:
                if name[-4:] == '.apk' and 'enjarify' in name:
                    apk_name = name
                    dex_path = path + 'enjarify\\'

        apk_path = path + apk_name
        print apk_path

        inside_file_list = os.listdir(path+'uncompress')
        dex_list = []
        for file in inside_file_list:
            if file[-4:] == '.dex':
                dex_list.append(file)
        print dex_list

        if len(dex_list) == 1:
            single_dex(dex_path)
        else:
            multi_dex(dex_path=dex_path, package_path=path,num=len(dex_list))

        f_p = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//after_pro.txt', 'a')
        f_p.write(package_list[i]+'\n')
        f_p.close()
        #break



if __name__ == '__main__':
    slove()