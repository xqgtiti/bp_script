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

def dex2jar(apk_name, nu):
    os.chdir(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name)
    comand_line = 'd2j-dex2jar.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//apk_uncompress//classes%s.dex"'%nu
    print comand_line
    dex2jar_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dex2jar_subp.wait()
    error, out = dex2jar_subp.communicate()
    return out

def jar2dex(apk_name, nu):
    comand_line = 'd2j-jar2dex.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//classes%s-dex2jar.jar"'%nu
    print comand_line
    jar2dex_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    jar2dex_subp.wait()
    error, out = jar2dex_subp.communicate()
    #print out
    return out

def enjarify(apk_name, nu):
    comand_line = 'enjarify.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//apk_uncompress//classxces%s.dex"'%nu
    print comand_line
    enjarify_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    enjarify_sub.wait()
    error, out = enjarify_sub.communicate()
    print out

def rm(file_name):
    comand_line = 'del '+file_name
    print comand_line
    rm_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    rm_sub.wait()
    error, out = rm_sub.communicate()
