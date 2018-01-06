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
    print shlex.split(comand_line)

    uncompress.wait()
    error, out = uncompress.communicate()
    return uncompress.returncode

def dex2jar(apk_name, num):
    os.chdir(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name)
    comand_line = 'd2j-dex2jar.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//apk_uncompress//classes%s.dex"'%num
    res_code = os.system(comand_line)
    print res_code
    return res_code
    """
    print comand_line
    dex2jar_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    dex2jar_subp.wait()
    error, out = dex2jar_subp.communicate()
    return out"""


def jar2dex(apk_name, file_name):
    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    comand_line = 'd2j-jar2dex.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//'+file_name+'"'
    print comand_line
    jar2dex_subp =  subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    jar2dex_subp.wait()
    error, out = jar2dex_subp.communicate()
    print out
    return out


def enjarify(apk_name,num):
    os.chdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name)
    comand_line = 'enjarify.bat "'+ PROGUARD_WORK_SPACE_WIN + 'dir_'+apk_name+'//apk_uncompress//classes%s.dex"'%num
    print comand_line
    enjarify_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    enjarify_sub.wait()
    error, out = enjarify_sub.communicate()
    print out

def rm(file_name):
    comand_line = 'del '+file_name
    rm_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    shell=True)
    rm_sub.wait()
    error, out = rm_sub.communicate()

def z7_dele(apk_name, file_name):
    comand_line = '7z d "%s" "%s"'%(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'//'+apk_name, file_name)
    #print comand_line
    z7_dele_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    z7_dele_sub.wait()
    error, out = z7_dele_sub.communicate()
    #print error
    #print out
    return z7_dele_sub.returncode

def z7_add(apk_name, file_name):
    #新的dex目录 /new/classes*.dex
    comand_line = '7z u "%s" "%s"'%(PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'//'+apk_name, PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'//new_dex//'+file_name)
    z7_add_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    z7_add_sub.wait()
    error, out = z7_add_sub.communicate()
    #print error
    #print out
    return z7_add_sub.returncode

def jarsign(apk_name, key_name, key_pass):
    #对apk进行签名
    comand_line = 'jarsigner -verbose -keystore "%s" -storepass %s "%s" "%s"'\
                  %(PROGUARD_WORK_SPACE_WIN+key_name,
                    key_pass,
                    PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '//' + apk_name,
                    key_name)
    os.system(comand_line)

    """
    print comand_line
    jarsign_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    jarsign_sub.wait()
    error, out = jarsign_sub.communicate()
    print error
    print out
    print jarsign_sub.returncode
    return jarsign_sub.returncode
    """

def jar(jar_name,dir_name, apk_name):
    comand_line = 'jar cvf %s -C %s .'%(jar_name, dir_name)
    print comand_line
    return_code = os.system(comand_line)
    comand_line = '7z d "%s" "%s"' % (PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '//' + 'classes_merge.jar', 'META-INF')
    os.system(comand_line)
    return return_code


