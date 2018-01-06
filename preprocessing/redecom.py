# -*- coding:utf-8 -*- 

"""
@author: xqg
@file: redecom.py
@time: 2018/1/4 15:07
@desc:

"""
import os
import sys
import shlex, subprocess
from global_path import *
import platform
import json
import time

from command import *
import commands
global ROOT_PATH #对100测试的根目录
global REDE_PATH #dex->jar, jar->dex再重新签名的目录

str_uncompress_success = 'uncompress success!'
str_uncompress_fail = 'uncompress fail...return'

jar2dex_error_str = ['trouble processing:','warning','Exception']
dex2jar_error_str = ['Detail Error Information','Exception']
enjarify_error_str = []

key_pass = 'zhuzhu66'
key_name = 'demo.keystore'

def jarsign(apk_path, key_path):

    comand_line = 'jarsigner -verbose -keystore "%s" -storepass %s "%s" "%s"'\
                  %(key_path,
                    key_pass,
                    apk_path,
                    key_name)
    res = os.system(comand_line)
    return int(res)

def z7_dele(apk_path, file_name):
    comand_line = '7z d "%s" "%s"'%(apk_path, file_name)
    res = os.system(comand_line)
    return int(res)

def z7_add(apk_path, file_path):
    #新的dex目录 /new/classes*.dex
    comand_line = '7z u "%s" "%s"'%(apk_path,file_path)
    res = os.system(comand_line)
    return int(res)

def shell_uncompress(file_path, save_path):
    # uncompress
    comand_line = '7z.exe x -r -y -aos -o"%s" "%s"' % (save_path, file_path)
    return_code = os.system(comand_line)

    return return_code

def shell_enjarify(current_path, dex_path):
    # 生成jar到当前目录下
    os.chdir(current_path)
    print current_path
    comand_line = 'enjarify "%s"' % dex_path
    print comand_line
    dex2jar_subp = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dex2jar_subp.wait()
    error, out = dex2jar_subp.communicate()

    if 'Error, output file already exists and --force was not specified.'.upper() in out.upper() \
            or 'Error, output file already exists and --force was not specified.'.upper() in error.upper():
        return 0
    if '0 classes had errors'.upper() in out.upper() or '0 classes had errors'.upper() in error.upper():
        return 0
    else:
        return error + '\n' + out + '\n'
def shell_dex2jar(current_path, dex_path):
    #生成jar到当前目录下
    os.chdir(current_path)
    comand_line = 'd2j-dex2jar "%s"'%dex_path

    dex2jar_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dex2jar_subp.wait()
    error,out = dex2jar_subp.communicate()


    for error_str in dex2jar_error_str:
        if error_str.upper() in out.upper() or error_str.upper() in error.upper():
            return error+'\n'+out+'\n'
    return 0

def shell_jar2dex(current_path, jar_path):
    #生成dex到当前目录下
    os.chdir(current_path)
    comand_line = 'd2j-jar2dex "%s"'%jar_path
    jar2dex_subp = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    jar2dex_subp.wait()
    error, out = jar2dex_subp.communicate()

    for error_str in jar2dex_error_str:
        if error_str.upper() in out.upper() or error_str.upper() in error.upper():
            return error+'\n'+out+'\n'
    return 0

def slove_all_dex2jar(current_path, uncompress_path, dex_list,f_exec_log):

    for dex in dex_list:
        num = dex[7:8]
        if num == '.': num = ""
        print '#! slove all in dex2jar classes%s.dex'%num
        return_code = shell_dex2jar(current_path, uncompress_path+dex)
        if return_code != 0:
            f_exec_log.write('---dex2jar classes%s.dex fail...return'%num+'\n')
            f_exec_log.write('Error Massage:\n' + return_code)
            return 0
        f_exec_log.write('---dex2jar classes%s.dex success!' % num + '\n')
        return_code = shell_jar2dex(current_path, current_path+'classes%s-dex2jar.jar'%num)

        if return_code != 0:
            f_exec_log.write('---jar2dex classes%s-dex2jar.jar fail...return'%num+'\n')
            f_exec_log.write('Error Massage:\n'+return_code)
            return 0
        f_exec_log.write('---jar2dex classes%s-dex2jar.jar success! '%num+'\n')

    return 1

def slove_all_enjarify(current_path, uncompress_path, dex_list,f_exec_log):

    for dex in dex_list:
        num = dex[7:8]
        if num == '.': num = ""
        print '#! slove all in enjarify classes%s.dex'%num

        copy_command = 'copy "%s" "%s"'%(uncompress_path+dex,current_path)
        os.system(copy_command)
        return_code = shell_enjarify(current_path, current_path+dex)
        if return_code != 0:
            f_exec_log.write('---enjarify classes%s.dex fail...return'%num+'\n')
            f_exec_log.write('Error Massage:\n' + return_code)
            return 0
        f_exec_log.write('---enjarify classes%s.dex success!' % num + '\n')
        return_code = shell_jar2dex(current_path, current_path+'classes%s-enjarify.jar'%num)

        if return_code != 0:
            f_exec_log.write('---jar2dex class%s-dex2jar.jar fail...return'%num+'\n')
            f_exec_log.write('Error Massage:\n'+return_code)
            return 0
        f_exec_log.write('---jar2dex class%s-dex2jar.jar success! '%num+'\n')

    return 1

def dele_pre_file_in_apk_and_put_new_dex(apk_path, len, new_dex_path):
    for i in range(1,1+len):
        if i == 1: num = ""
        else: num = str(i)
        print num
        return_code = z7_dele(apk_path=apk_path,file_name='classes%s.dex'%num)
        if return_code != 0: return 0
        return_code = z7_add(apk_path=apk_path,file_path=new_dex_path+'classes%s.dex'%num)
        if return_code != 0: return 0
    return_code = z7_dele(apk_path=apk_path,file_name='META-INF')
    if return_code != 0: return 0
    return 1


def slove_win(package_name):
    print '#! begin slove '+package_name+':\n'
    package_path = REDE_PATH + package_name + '\\'
    file_list = os.listdir(package_path)
    apk_name = ""
    for file in file_list:
        if file[-4:] == '.apk': apk_name = file
    init_apk_file = package_path + apk_name
    ans_dict = {}
    final_ans_dict = {}
    final_ans_dict['enjarify'] = 0
    final_ans_dict['dex2jar'] = 0
    f_exec_log = open(package_path + 'exec_log_' + str(int(time.time())) + '.txt', 'w')
    f_exec_log.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\n')


    # 1.解压缩
    uncompress_path = package_path+ 'uncompress\\'
    if os.path.exists(uncompress_path) == True:
        f_exec_log.write('---'+str_uncompress_success + '\n')
        gd = 1
    else:
        return_code = shell_uncompress(init_apk_file,uncompress_path)
        if return_code != 0:
            #解压失败
            f_exec_log.write('---'+str_uncompress_fail+'\n')
            return
        f_exec_log.write('---'+str_uncompress_success+'\n')
    uncompress_list = os.listdir(uncompress_path)
    dex_list = []
    for file_name in uncompress_list:
        if file_name[-4:] == '.dex': dex_list.append(file_name)

    print '#! uncompress done!'

    #新建处理dex2jar目录
    dex2jar_path = package_path + 'dex2jar\\'
    dex2jar_newdex_path = package_path + 'dex2jar_newdex\\'
    if os.path.exists(dex2jar_path) == False: os.mkdir(dex2jar_path)
    if os.path.exists(dex2jar_newdex_path) == False: os.mkdir(dex2jar_newdex_path)
    f_exec_log.write('---mkdir dex2jar,dex2jar_newdex!'+'\n')
    return_code = slove_all_dex2jar(dex2jar_path, uncompress_path, dex_list,f_exec_log)
    if return_code == 0:
        f_exec_log.write('===dex2jar and jar2dex all classes.dex fail....===\n\n')
        ans_dict['dex2jar'] = 0
    else:
        f_exec_log.write('===dex2jar and jar2dex all classes.dex success!!!===\n\n')
        ans_dict['dex2jar'] = 1

    print '#! dex2jar done!'

    #新建处理enjarify目录
    enjarify_path = package_path + 'enjarify\\'
    enjarify_newdex_path = package_path + 'enjarify_newdex\\'
    if os.path.exists(enjarify_path) == False: os.mkdir(enjarify_path)
    if os.path.exists(enjarify_newdex_path) == False: os.mkdir(enjarify_newdex_path)
    f_exec_log.write('mkdir enjarify,enjarify_newdex!'+'\n')
    return_code = slove_all_enjarify(enjarify_path,uncompress_path,dex_list,f_exec_log)
    if return_code == 0:
        f_exec_log.write('===enjarify and jar2dex all classes.dex fail....===\n\n')
        ans_dict['enjarify'] = 0
    else:
        f_exec_log.write('===enjarify and jar2dex all classes.dex success!!!===\n\n')
        ans_dict['enjarify'] = 1

    print '#! enjarify done!'

    if ans_dict['dex2jar'] == 1:
        #把新的文件复制到目录下
        for i in range(1,1+len(dex_list)):
            if i == 1: num = ""
            else: num = str(i)
            copy_command = 'copy %s %s'%(dex2jar_path+'classes%s-dex2jar-jar2dex.dex'%num,dex2jar_newdex_path+'classes%s.dex'%num)
            if os.path.exists(dex2jar_newdex_path+'classes%s.dex'%num) == False: os.system(copy_command)
        f_exec_log.write('---copy all new dex to dex2jar_newdex dir!\n')

        dex2jar_apk_path = package_path+'dex2jar_'+apk_name
        if os.path.exists(dex2jar_apk_path) == False:
            copy_command = 'copy "%s" "%s"'%(init_apk_file,dex2jar_apk_path)
            os.system(copy_command)
        f_exec_log.write('---copy apk to dex2jar_apk!\n')

        # 删去原来的签名和dex,放入新文件
        return_code = dele_pre_file_in_apk_and_put_new_dex(dex2jar_path, len(dex_list), dex2jar_newdex_path)
        if return_code == 0:
            f_exec_log.write('---dele pre file in dex2jar_apk and put new dex fail...\n')
        else:
            f_exec_log.write('---dele pre file in dex2jar_apk and put new dex success!\n')

            # 重新签名
            return_code = jarsign(dex2jar_apk_path, ROOT_PATH + key_name)
            if return_code != 0:
                f_exec_log.write('---resigin dex2jar apk fail...\n')
            else:
                f_exec_log.write('===resigin dex2jar apk fail success!!!\n\n')
                final_ans_dict['dex2jar'] = 1


    if ans_dict['enjarify'] == 1:
        for i in range(1,1+len(dex_list)):
            if i == 1: num = ""
            else: num = str(i)
            copy_command = 'copy %s %s'%(enjarify_path+'classes%s-enjarify-jar2dex.dex'%num,enjarify_newdex_path+'classes%s.dex'%num)
            if os.path.exists(enjarify_newdex_path+'classes%s.dex'%num) == False: os.system(copy_command)
        f_exec_log.write('---copy all new dex to enjarify_newdex dir!\n')

        enjarify_apk_path = package_path+'enjarify_'+apk_name
        if os.path.exists(enjarify_apk_path) == False:
            copy_command = 'copy "%s" "%s"'%(init_apk_file,enjarify_apk_path)
            os.system(copy_command)
        f_exec_log.write('---copy apk to enjarify_apk!\n')

        #删去原来的签名和dex,放入新文件
        return_code = dele_pre_file_in_apk_and_put_new_dex(enjarify_apk_path,len(dex_list),enjarify_newdex_path)
        if return_code == 0:
            f_exec_log.write('---dele pre file in enjarify_apk and put new dex fail...\n')
            return final_ans_dict
        f_exec_log.write('---dele pre file in enjarify_apk and put new dex success!\n')

        #重新签名
        return_code = jarsign(enjarify_apk_path,ROOT_PATH+key_name)
        if return_code != 0:
            f_exec_log.write('---resign enjarify apk fail...\n')
            return final_ans_dict
        f_exec_log.write('===resign enjarify apk fail success!!!\n\n')
        final_ans_dict['enjarify'] = 1

    f_final_ans = open(package_path+'process_results.txt','w')
    f_final_ans.write(json.dumps(final_ans_dict,ensure_ascii=False)+'\n')
    f_final_ans.close()
    f_exec_log.close()
    return final_ans_dict
def slove_macos(apk_name):
    gd = 1


def SLOVE_ALL(st,ed):
    package_list = os.listdir(REDE_PATH)

    f_xapk = open(TOP_100_PATH + 'xapk.txt')
    f_resign_fail = open(TOP_100_PATH + 'resign_fail.txt')
    f_done = open(ROOT_PATH + 'rede_and_resigin_done_apk.txt', 'rb')

    resign_fail_table = {}
    xapk_table = {}
    done_table = {}
    while True:
        r = f_xapk.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        xapk_table[res['package_name']] = 1

    while True:
        r = f_resign_fail.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        resign_fail_table[r] = 1

    while True:
        r = f_done.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        done_table[r] = 1

    dict = {}
    for name in package_list:

        xh = ""
        for i in name:
            if i.isdigit() == True:
                xh = xh + i
            else:
                break
        dict[int(xh)] = name

    ll = sorted(dict.items(), key=lambda d: d[0])

    for i in range(st, ed):
        path = REDE_PATH + ll[i][1] + '\\'
        package_name = ll[i][1]

        #如果是xapk，则先排除
        try:
            if xapk_table[ll[i][1]] == 1:
                print 'xapk continue'
                continue
        except: gd = 1

        #如果已经处理过，排除
        try:
            if done_table[ll[i][1]] == 1:
                print 'already continue'
                continue
        except: gd = 1

        #如果重新签名失败，排除
        try:
            if resign_fail_table[ll[i][1]] == 1:
                print 'resigin fail continue'
                continue
        except: gd = 1

        #如果重新签名失败，也要排除
        f_done = open(ROOT_PATH + 'rede_and_resigin_done_apk.txt', 'a')
        res = slove_win(package_name)
        f_done.write(package_name+'\n')
        f_done.close()

def cal():
    f = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_and_resigin_done_apk.txt','rb')
    package_list = []
    while True:
        r = f.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        package_list.append(r)
    f.close()
    cnt = 0
  #  f_to_install = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST\\rede_to_install.txt','w')
    for package_name in package_list:
        #print package_name
        try:
            f = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST\REDE_AND_RESIGIN\\'+package_name+'\\'+'process_results.txt','rb')
            r = f.readline()
            r = r.strip('\r')
            res = eval(r)
            #print res
            #if res['enjarify'] == 1 or res['dex2jar'] == 1:
                #f_to_install.write(package_name+'\n')
            if res['enjarify'] == 0 and res['dex2jar'] == 1:
                print '???????'
        except:
            continue
       # break
    print cnt

def install_apk(apk_path):
    comand_line = 'adb install "%s"'%apk_path
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    install_apk_sub.wait()
    out, error = install_apk_sub.communicate()

    if 'adb: failed to install' in error:
        return 0
    elif 'Success' in out: return 1
    else:
        return error

def install_rede(st,ed):

    package_list = []
    f_fail = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_install_fail.txt','a')

    f_package = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_to_install.txt','rb')
    while True:
        r = f_package.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        package_list.append(r)

    for i in range(st, ed):
        path = REDE_PATH+package_list[i]+'\\'
        f_res = open(path+'process_results.txt')
        r = f_res.readline()
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        inside_list = os.listdir(path)
        apk_name = ""
        if res['dex2jar'] == 1:
            for name in inside_list:
                if name[-4:] == '.apk' and 'dex2jar' in name:
                    apk_name = name
        else:
            for name in inside_list:
                if name[-4:] == '.apk' and 'enjarify' in name:
                    apk_name = name

        apk_path = path + apk_name
        print apk_path

        return_code = install_apk(apk_path=apk_path)
        if return_code != 1:
            print return_code
            f_fail.write(package_list[i] + '\n')
            continue
        else:
            print 'success!'
        print '-------------------'

def cal_final_rest():
    f_shantui = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//shantui.txt','rb')
    dict = {}
    while True:
        r = f_shantui.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        dict[r] = 1

    f_final = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_final.txt','w')
    f_install = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_to_install.txt','rb'
                     )
    while True:
        r = f_install.readline()
        if not r:break
        r = r[:-1]
        r = r.strip('\r')

        try:
            if dict[r] == 1: continue
        except:
            f_final.write(r+'\n')

if __name__ == '__main__':
    cal_final_rest()
    """
    if platform.system() == 'Windows':
        ROOT_PATH = 'G:\PROGUARD_WORK_SPACE\TOP100_TEST\\'
        REDE_PATH = ROOT_PATH + 'REDE_AND_RESIGIN\\'
        install_rede(40,60)
        #cal()
        #SLOVE_ALL(0,100)
        #res = slove_win('3_com.lenovo.anyshare.gps')
        #print res
    """
