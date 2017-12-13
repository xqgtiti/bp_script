# -*- coding:utf-8 -*- -
import os
import shutil
import platform
import sys
import datetime
import shlex, subprocess

from global_path import *

reload(sys)
sys.setdefaultencoding('utf-8')

def compress(compress_name, file_path):
    comand_line = '7z.exe a -r "%s" "%s"'%(compress_name,file_path)
    compress = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    compress.wait()
    return compress.returncode

def uncompress(file_path, save_path):
    #uncompress
    comand_line = '7z.exe x -r -y -aos -o"%s" "%s"'%(save_path,file_path)
    print comand_line
    uncompress = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    uncompress.wait()
    error, out = uncompress.communicate()
    return uncompress.returncode

def dex2jar(apk_name):
    os.chdir(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name)
    comand_line = 'd2j-dex2jar.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//apk_uncompress//classes.dex"'
    print comand_line
    dex2jar_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dex2jar_subp.wait()
    error, out = dex2jar_subp.communicate()
    return out

def jar2dex(apk_name):
    a = 1