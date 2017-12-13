# -*- coding:utf-8 -*- -
import os
import shutil
import platform
import sys
import datetime
import shlex, subprocess

from global_path import *
from command import *
from dex_process.single_dex import *
from dex_process.multi_dex import *
from androguard.core.bytecodes import apk

reload(sys)
sys.setdefaultencoding('utf-8')
def slove_windows():

    ROOT_PATH = 'C://Users//xqg//Desktop//mutildex'
   # root_path = 'C://Users//xqg//Desktop//mutildex'
    list = os.listdir(root_path)

    f_out = open(root_path + '//map_out.txt', 'w')  # 映射文件
    merge_dir_path_root = 'C://Users//xqg//Desktop//mutildex//classes_merge//'
    if os.path.exists(merge_dir_path_root) == False:
        os.makedirs(merge_dir_path_root)
    for i in range(0, len(list)):
        path = os.path.join(root_path, list[i])

        if os.path.isdir(path) == True and '-dex2jar' in path:
            print path
            print len(path)
            xh = path[-9:-8]
            for root, dirs, files in os.walk(path, 'rb'):
                for dir in dirs:
                    dirPath = str(os.path.join(root, dir))
                    dir_inside = str(os.path.join(root[len(path) + 1:], dir))
                    merge_dir_path = merge_dir_path_root + dir_inside
                    if os.path.exists(merge_dir_path) == False:
                        print 'make dir:' + merge_dir_path
                        os.makedirs(merge_dir_path)

                for file in files:
                    filePath = str(os.path.join(root, file))
                    file_inside = str(os.path.join(root[len(path) + 1:], file))
                    merge_file_path = merge_dir_path_root + file_inside
                    f_out.write(xh + ':' + merge_file_path + '\n')
                    if os.path.exists(merge_file_path) == False:
                        print 'cp file:' + merge_file_path
                        shutil.copyfile(filePath, merge_file_path)
                    # print os.path.isdir(filePath)
                # shutil.copyfile(filePath,os.path.join(merge_dir_path,file))

        # break

def test(apk_name):
    return_code = uncompress(PROGUARD_WORK_SPACE_WIN+apk_name,PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/apk_uncompress')
    if int(return_code) != 0:
        #uncompress fail
        f_fail = open(PROGUARD_WORK_SPACE_WIN+'fail_log//'+apk_name+'.txt','w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S')+'\n'+apk_name+'\n'+'Uncompress APK Fail'+'\n')
        f_fail.close()
        return

    apk_uncompress_path = PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name+'/apk_uncompress'
    list = os.listdir(apk_uncompress_path)
    print list
    class_dex_cnt = 0
    for file in list:
        if 'classes' in file and '.dex' in file:
            class_dex_cnt = class_dex_cnt + 1
    print class_dex_cnt

    if class_dex_cnt == 1:
        single_dex(apk_name)
    else:
        gd = 1

if __name__ == '__main__':
    test('com.jonathanrobins.pepe_snap.apk')

