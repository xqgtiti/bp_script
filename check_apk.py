# -*- coding:utf-8 -*- -
import os
from global_path import *
import json
import shlex, subprocess
def z7_dele(apk_path, file_name):
    comand_line = '7z d "%s" "%s"'%(apk_path, file_name)
    z7_dele_sub = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    z7_dele_sub.wait()
    error, out = z7_dele_sub.communicate()
    return z7_dele_sub.returncode
if __name__ == '__main__':

    apk_path = APK_SOTRAGE_PATH
    xapk_xh = {}
    #{序号:包名}
    list = os.listdir(apk_path)
    print list

    dict = {}
    for name in list:

        xh = ""
        for i in name:
            if i.isdigit() == True:
                xh = xh + i
            else: break
        dict[int(xh)] = name
    ll = sorted(dict.items(), key=lambda d: d[0])

    f = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//xapk.txt','w')
    for i in range(0,100):
        path = apk_path + ll[i][1]
        list_in_dir = os.listdir(path)
        if len(list_in_dir) != 1:
            print path
        if list_in_dir[0][-4:] != '.apk':
            print list_in_dir[0][-4:]
            print list_in_dir[0]
            xapk_xh[i+1] = ll[i][1]
            save_table = {}
            save_table['rank'] = i + 1
            save_table['package_name'] = ll[i][1]
            f.write(json.dumps(save_table,ensure_ascii=False)+'\n')
    print xapk_xh
