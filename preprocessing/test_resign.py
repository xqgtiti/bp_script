# -*- coding:utf-8 -*- -
import os
import sys
import shlex, subprocess
from global_path import *
reload(sys)
sys.setdefaultencoding('gbk')
key_path = 'G:\PROGUARD_WORK_SPACE\TOP100_TEST\\demo.keystore'
def z7_dele(apk_path, file_name):
    comand_line = '7z d "%s" "%s"'%(apk_path, file_name)
    res = os.system(comand_line)
    return int(res)
def jarsign(apk_path, key_path, key_pass, key_name):
    #对apk进行签名
    comand_line = 'jarsigner -verbose -keystore "%s" -storepass %s "%s" "%s"'\
                  %(key_path,
                    key_pass,
                    apk_path,
                    key_name)
    res = os.system(comand_line)
    return int(res)
def del_pre_sign():
    f_fail = open(TOP_100_PATH + 'resign_fail.txt','w')
    f_xapk = open(TOP_100_PATH + 'xapk.txt')
    xapk_table = {}
    while True:
        r = f_xapk.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        xapk_table[res['package_name']] = 1

    resign_path = TOP_100_PATH + 'RESIGN_ONLY\\'
    package_list = os.listdir(resign_path)

    cnt = 0
    for package in package_list:
        cnt = cnt + 1
        print cnt
        print package
        print '......................................................'

        try:
            if xapk_table[package] == 1:
                print 'xapk continue....'
                continue
        except:
            a = 1
        dir_path = resign_path + package + '\\'
        inside_list = os.listdir(dir_path)

        apk_name = ''
        if 'resigin_' in inside_list[0]:
            apk_name = inside_list[0]
        else:
            apk_name = inside_list[1]

        print '????'
        print apk_name
        return_code =  z7_dele(dir_path+apk_name,'META-INF')
        if return_code != 0:
            f_fail.write(package + '\n')
            continue

        return_code =jarsign(apk_path=dir_path+apk_name, key_path=key_path,
                             key_pass='zhuzhu66',key_name='demo.keystore')
        if return_code != 0:
            f_fail.write(package + '\n')
            continue


def uninstall_apk(apk_name):
    comand_line = 'adb install "%s"' % apk_name
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    install_apk_sub.wait()
    out, error = install_apk_sub.communicate()

    if 'adb: failed to install' in error:
        return 0
    elif 'Success' in out:
        return 1
    else:
        return error

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

def install(st, ed):
    f_fail = open(TOP_100_PATH + 'resign_install_fail.txt', 'a')
    f_xapk = open(TOP_100_PATH + 'xapk.txt')
    xapk_table = {}
    while True:
        r = f_xapk.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        xapk_table[res['package_name']] = 1

    resign_path = TOP_100_PATH + 'RESIGN_ONLY\\'
    package_list = os.listdir(resign_path)

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
        path = resign_path + ll[i][1]+'\\'

        try:
            if xapk_table[ll[i][1]] == 1:
                print 'xapk continue'
                continue
        except: gd = 1
        inside_list = os.listdir(path)
        if 'resign_' in inside_list[0]: apk_name = inside_list[0]
        else: apk_name = inside_list[1]

        apk_path = path + apk_name

        print i
        print apk_path
        return_code = install_apk(apk_path=apk_path)
        if return_code != 1:
            print return_code
            f_fail.write(ll[i][1] + '\n')
            continue
        else:
            print 'success!'
        print '-------------------'

def decompile_all(apk_name):
    a = 1

if __name__ == '__main__':
    install(70,90)
    """
    f_xapk = open(TOP_100_PATH + 'xapk.txt')
    xapk_table = {}
    while True:
        r = f_xapk.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        xapk_table[res['package_name']] = 1

    resign_path = TOP_100_PATH + 'RESIGN_ONLY\\'
    package_list = os.listdir(resign_path)

    cnt = 0
    for package in package_list:
        cnt = cnt + 1
        print cnt
        try:
            if xapk_table[package] == 1:
                print 'xapk continue....'
                continue
        except:
            a = 1
        dir_path = resign_path + package + '\\'
        inside_list = os.listdir(dir_path)
        apk_path = dir_path + inside_list[0]
        os.system('copy "%s" "%s"' % (apk_path, dir_path + 'resign_' + inside_list[0]))
    """
   # del_pre_sign()