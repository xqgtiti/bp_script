# -*- coding:utf-8 -*- -
import os
import shlex, subprocess

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


if __name__ == '__main__':

    res = install_apk('D:\BTS Messenger_v1.1_apkpure.com.apk')
    print res
