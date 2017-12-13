# -*- coding:utf-8 -*- -
import os
import shutil
import platform
import sys
import datetime
import shlex, subprocess
reload(sys)

sys.setdefaultencoding('utf-8')
PROGUARD_WORK_SPACE_WIN = 'F:\PROGUARD_WORK_SPACE\TOTAL_APK_ROOT_GOOGLE\\'
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

def zip(zip_name, file_path):
    comand_line = '7z.exe a -r "%s" "%s"'%(zip_name,file_path)
    zip = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    zip.wait()
    return zip.returncode

def unzip(file_path, save_path):
    #完整路径下解压
    comand_line = '7z.exe x -r -y -aos -o"%s" "%s"'%(save_path,file_path)
    print comand_line
    unzip = subprocess.Popen(shlex.split(comand_line), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    unzip.wait()
    error, out = unzip.communicate()
    return unzip.returncode

def test(apk_name):
    return_code = unzip(PROGUARD_WORK_SPACE_WIN+apk_name,PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name)

    if int(return_code) != 0:
        #解压失败，记录到日志
        f_fail = open(PROGUARD_WORK_SPACE_WIN+'fail_log//'+apk_name+'.txt','w')
        now = datetime.datetime.now()
        f_fail.write(now.strftime('%Y-%m-%d %H:%M:%S')+'\n'+apk_name+'\n'+'Uncompress Fail'+'\n')
        f_fail.close()
        return

    apk_uncompress_path = PROGUARD_WORK_SPACE_WIN+'dir_'+apk_name
    list = os.listdir(apk_uncompress_path) #列出文件夹下所有的目录与文件
    print list
    class_dex_cnt = 0
    for file in list:
        if 'classes' in file and '.dex' in file:
            class_dex_cnt = class_dex_cnt + 1
    print class_dex_cnt

if __name__ == '__main__':
    import subprocess
    test('com.jonathanrobins.pepe_snap.apk')
    #
    #ping = subprocess.Popen(["ping", "127.0.0.1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #out, error = ping.communicate()
    #print(out.decode('gbk'))  # gbk是我电脑上的编码，你可以试试其他的

