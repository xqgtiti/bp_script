# -*- coding:utf-8 -*- -
import sys
import os
import shlex, subprocess

from global_path import *
reload(sys)
sys.setdefaultencoding('utf-8')
def shrink(apk_name):
    f = open('F:\PROGUARD_WORK_SPACE\TOTAL_APK_ROOT_GOOGLE\dir_%s//android_single_dex.pro'%apk_name,'a')

    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    comand_line = 'java -jar "D:\workspace\\big_program\\tool\proguard5.3.3\lib\proguard.jar" @android_single_dex.pro'
    os.system(comand_line)
    """
    print comand_line
    proguard_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    proguard_sub.wait()
    error, out = proguard_sub.communicate()
    print error
    print out
    """
if __name__ == '__main__':
    shrink('com.jonathanrobins.pepe_snap.apk')