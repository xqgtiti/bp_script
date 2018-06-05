# -*- coding:utf-8 -*- -
import re
import os
import shlex, subprocess
import re
import threading
import time
import signal
import multiprocessing
import time
from global_path import *
PUMA_PATH = 'D:\Bwork\ontry\PUMA-master\\'
ANS_PATH = 'G:\dfive\\ex3\\'
import json

global PACKAGE_NAME
global LABEL_NAME

PACKAGE_NAME = ''
LABEL_NAME = ''

from command import *
#from multi_dex import *
#from single_dex import *


def setup_phone():

    os.system('adb shell "rm -rf /data/local/tmp/*"')
    os.system('adb push %shaos /data/local/tmp' % PUMA_PATH)
    os.system('adb shell "chmod 0755 /data/local/tmp/haos"')
    os.system('adb shell "ls -l /data/local/tmp/haos"')
    os.system('adb shell "mkdir -p /data/local/tmp/local/tmp"')


def get_app_info(apk_path):
    global PACKAGE_NAME
    global LABEL_NAME

    # get app label and package name

    comand_line = 'aapt dump badging "%s"' % apk_path
    get_package_name_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True)

    out, error = get_package_name_sub.communicate()
    ret = re.findall(r"application-label:'.*'", out)
    ll = ret[0].split("'")
    label_name = ll[1]

    ret = re.findall(r"package: name='.*'", out)
    ll = ret[0].split("'")
    package_name = ll[1]

    f = open('app.info', 'w')
    f.write(package_name + '\n')
    f.write(label_name + '\n')

    f.close()
    os.system('adb push app.info /data/local/tmp/')

    PACKAGE_NAME = package_name
    LABEL_NAME = label_name

    if PACKAGE_NAME == '' or LABEL_NAME == '':
        print('Fail to get app info.' + '\n')
        return "-1"

    return PACKAGE_NAME, LABEL_NAME


def install(apk_name):
    comand_line = 'adb install "%s"' % apk_name
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    out, error = install_apk_sub.communicate()

    #print out
    #print error

    if 'Failure' in out:
        print('Failed to install.')
        if 'INSTALL_FAILED_ALREADY_EXISTS' in out:
            print('Already be installed.')
            gd = 1
            return 1
        else:
            gd = 1
            return 0
    elif 'Success' in out:
        print('Install success.')
        return 1


def uninstall(apk_name):

    comand_line = 'adb uninstall "%s"' % apk_name
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    out, error = install_apk_sub.communicate()

def run(package_name):

    os.system('run.sh')
    os.system('adb push bin/TestApp.jar /data/local/tmp/')

    p = multiprocessing.Process(target=use_puma)
    p.start()

    p.join(60*3)  # wait 3 minutes

    #  print 'package_name'
    #  print package_name
    if p.is_alive():

        print("still running... let's kill it...")
        print(package_name)

        p.terminate()
        p.join()

        # close the running app
        os.system('adb shell "am force-stop %s"' % package_name)
        # 把android系统中的puma进程结束掉
        os.system('kill_puma.sh')

        uninstall(apk_name=package_name)
        return 1

    else:

        uninstall(apk_name=package_name)
        return 0



def use_puma():

    content = os.popen('adb shell /data/local/tmp/haos runtest TestApp.jar -c nsl.stg.tests.LaunchApp').read()
    print content

def slove(apk_path):
    package_name = get_app_info(apk_path)

    if package_name == "-1":
        print("No app package name or app label")

    else:
        run(package_name)


def SLOVE():

    setup_phone()
    PUMA_PATH = 'D:\Bwork\ontry\PUMA-master'
    os.chdir(PUMA_PATH)

    apk_path = 'G:\Nwork\DK\\apks\\3\\2_tat.example.ildar.seer\\PoliceDetectorSpeedCameraRadar_v1.6_apkpure.com.apk'
    res = install(apk_path)

    if res == 0:
        print '安装失败'
    else:
        slove(apk_path)

def test_install_pre(apk_path):

    global PACKAGE_NAME
    global LABEL_NAME

    comand_line = 'adb install "%s"' % apk_path
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    out, error = install_apk_sub.communicate()

    if 'Failure' in out:
        print '安装失败'
        if 'INSTALL_FAILED_ALREADY_EXISTS' in out:
            print '重复安装'
            return 1, 'Install Success'
        else:
            return 0, out
    elif 'Success' in out:
        print '安装成功'
        return 1, 'Install Success'


def process_apk(package_name, apk_name, f_log):
    return_code = uncompress(APKS_PATH + package_name + '\\' + apk_name,
                             APKS_PATH + package_name + '\\apk_uncompress')
    if int(return_code) != 0:
        now = datetime.datetime.now()
        f_log.write(now.strftime('%Y-%m-%d %H:%M:%S') + '\n' + apk_name + '\n' + 'Uncompress APK Fail' + '\n')
        return

    apk_uncompress_path = APKS_PATH + package_name + '\\apk_uncompress'
    list = os.listdir(apk_uncompress_path)
    class_dex_cnt = 0
    for file in list:
        if 'classes' in file and '.dex' in file:
            class_dex_cnt = class_dex_cnt + 1

    print class_dex_cnt
    # single_dex的情况

    if class_dex_cnt == 1:
        f_log.write('APK_NAME:' + apk_name + '(%s)' % 'single-dex')
        print ('APK_NAME:' + apk_name + '(%s)' % 'single-dex')
        single_res = single_dex(apk_name=apk_name, package_name=package_name, f_log=f_log)
        if single_res != 1:
            f_fail = open(APKS_PATH + package_name + '\\proguard_process_fail.txt', 'a')
            f_fail.close()

    else:
        f_log.write('This apk is multi-dex.' + '\n')
        multi_res = multi_dex(apk_name=apk_name, package_name=package_name, num=class_dex_cnt, f_log=f_log)
        if multi_res != 1:
            f_fail = open(APKS_PATH + package_name + '\\proguard_process_fail.txt', 'a')
            f_fail.close()


def all(apk_name, apk_path, package_name, package_path):
    global PACKAGE_NAME
    global LABEL_NAME

    f_log = open(package_path + 'run_log.txt', 'w')

    # 先初始化模拟器需要的目录
    setup_phone()

    # 获取app的信息
    get_app_info(apk_path)

    if PACKAGE_NAME == '' or LABEL_NAME == '':
        f_log.write('Get App Info Fail.' + '\n')
        return

    # 尝试安装
    res_code, res_text = test_install(apk_path)
    if res_code == 0:
        f_log.write('Test Install Fail.' + '\n')
        f_log.write('Error Message:' + '\n' + res_text)
        return
    os.system('adb uninstall %s' % PACKAGE_NAME)  # 卸载尝试的安装
    f_log.write('Test Install Success.' + '\n')

    # 如果可以安装成功,则开始使用proguard进行代码缩减
    process_apk(apk_name=apk_name, package_name=package_name, f_log=f_log)

    f_log.close()


def test_install(apk_path):

    #Test whether the original app can be installed in Android 4.3 device successfully.
    log_info("=== TEST INSTALL BEGIN ===\n")

    comand_line = 'aapt dump badging "%s"' % apk_path
    get_package_name_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True)
    out, error = get_package_name_sub.communicate()

    ret = re.findall(r"package: name='.*'", out)
    try:
        ll = ret[0].split("'")
        package_name_info = ll[1]
    except:
        package_name_info = ""

    if package_name_info == "":
        print('No package name.')
        log_info('No package name..\n')
        log_info("=== TEST INSTALL END ===\n\n")
        return 0

    comand_line = 'adb install "%s"' % apk_path
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    out, error = install_apk_sub.communicate()

    if 'Failure' in out:
        if 'INSTALL_FAILED_ALREADY_EXISTS' in out:
            print('Already be installed.')
            log_info('Already be installed.\n')
            comand_line = 'adb uninstall "%s"' % package_name_info
            install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                               shell=True)
            out, error = install_apk_sub.communicate()
            log_info("=== TEST INSTALL END ===\n\n")
            return 1
        else:
            print('Fail to install.')
            log_info('Fail to install.\n')
            log_info("=== TEST INSTALL END ===\n\n")
            return 0
    elif 'Success' in out:
        print('Install success')
        log_info('Install success.\n')
        comand_line = 'adb uninstall "%s"' % package_name_info
        install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           shell=True)
        out, error = install_apk_sub.communicate()
        log_info("=== TEST INSTALL END ===\n\n")
        return 1

def test_puma(apk_path):



def for_puma(apk_path, package_name, label_info, package_info):
    comand_line = 'adb install "%s"' % apk_path
    install_apk_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       shell=True)
    out, error = install_apk_sub.communicate()

    setup_phone()
    PUMA_PATH = 'D:\Bwork\ontry\PUMA-master'
    os.chdir(PUMA_PATH)

    f = open('app.info', 'w')
    f.write(package_info + '\n')
    f.write(label_info + '\n')

    f.close()
    os.system('adb push app.info /data/local/tmp/')

    return run(package_info)


def process_single_app(app_dir_path, apk_file_path):

    f_log = open(LOG_FILE,'a')

    return_code = test_install(apk_file_path)
    if return_code == 0:
        print('*** Fail in installation test. ***')
        log_info('*** Fail in installation test. ***\n')
        return 0

    return_code = test_puma(apk_file_path)


if __name__ == '__main__':

    process_single_app(apk_file_path=TEST_APP_PATH, app_dir_path=TEST_APP_DIR)

    """
    package_table = {}
    label_table = {}
    have_table = {}
    f_have = open('G:\Nwork\DK\puma\\puma_init_res.txt', 'rb')
    while True:
        r = f_have.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        have_table[res['package_name']] = 1
    f_have.close()
    f_info = open('G:\Nwork\DK\puma\\apk_info.txt', 'rb')
    while True:
        r = f_info.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)

        package_table[res['package_name']] = res['package_name_info']
        label_table[res['package_name']] = res['application_label_info']
    f_info.close()

    table = {}
    f = open('G:\Nwork\DK\puma\\install_init_res.txt', 'rb')
    while True:
        r = f.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        if res['res'] == 1:
            table[res['package_name']] = 1

    APK_PATH = 'G:\Nwork\DK\\apks\\'

    for i in range(0, 19):

        dir_path = APK_PATH + str(i + 1) + '\\'
        package_list = os.listdir(dir_path)
        cnt = 0
        for package_name in package_list:

            print str(i) + ' ' + str(package_name)
            ll1 = package_name.split('_')
            num = int(ll1[0])
            if num > 60: continue

            package_name_only = ll1[1]
            try:
                if table[package_name_only] == 1:
                    gd = 1
            except:
                continue
                gd = 1
            try:
                if have_table[package_name_only] == 1:
                    print '操作过'
                    continue
            except:
                gd = 1

            ll = package_name.split('_')
            package_path = dir_path + package_name + '\\'
            apk_path = package_path + os.listdir(package_path)[0]

            res = for_puma(apk_path, package_name_only, label_table[package_name_only],
                           package_table[package_name_only])

            saveTable = {}
            saveTable['res'] = res
            saveTable['package_name'] = package_name_only

            fsave = open('G:\Nwork\DK\puma\\puma_init_res.txt', 'a')
            fsave.write(json.dumps(saveTable, ensure_ascii=False) + '\n')
            fsave.close()
            # break
        # break

    """
    """
    list = os.listdir(APKS_PATH)

    cnt = 0
    for package_name in list:
        cnt = cnt + 1

        list_in = os.listdir(APKS_PATH+package_name)

        print str(cnt)+':'+package_name+':'

        if package_name == '179_com.vsco.cam': continue
        if 'proguard_process_done.txt' in list_in:
            print '此APP已经操作过 continue'
        elif 'proguard_process_fail.txt' in list_in:
            print '此APP已经操作过 且失败 continue'
        elif len(list_in) != 1:
            apk_name = ''
            for file_name in list_in:
                if file_name[-4:] == '.apk':
                    apk_name = file_name
                    break
                if file_name[-5:] == '.xapk':
                    print '这是xapk文件 continue'
                    break
            if apk_name != '':
                print '找到apk name'
                all(apk_name=apk_name,
                    apk_path=APKS_PATH + package_name + '\\%s' % apk_name,
                    package_path=APKS_PATH + package_name + '\\',
                    package_name=package_name)


        elif len(list_in) == 1:
            if '.xapk' in list_in[0]:
                print '这是xapk文件 continue'
                continue
            else:
                apk_name = list_in[0]
                all(apk_name=apk_name,
                    apk_path=APKS_PATH + package_name + '\\%s'%apk_name,
                    package_path=APKS_PATH + package_name + '\\',
                    package_name=package_name)

       # if package_name == '19_com.typany.ime':
       #     break
    """

