# -*- coding:utf-8 -*- 

"""
@author: xqg
@file: draw.py
@time: 2018/1/5 5:49
@desc:

"""
"""
Demo of the `streamplot` function.

A streamplot, or streamline plot, is used to display 2D vector fields. This
example shows a few features of the stream plot function:

    * Varying the color along a streamline.
    * Varying the density of streamlines.
    * Varying the line width along a stream line.
"""
ROOT_PATH = 'G:\PROGUARD_WORK_SPACE\TOP100_TEST\\'
REDE_PATH = ROOT_PATH + 'REDE_AND_RESIGIN\\'
import numpy as np
import os
import json
def cal_all():
    package_list = []

    fsave = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//size_sta.txt','w')
    f_package = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//rede_final.txt', 'rb')
    while True:
        r = f_package.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        package_list.append(r)
    print package_list

    xh = 0
    tot = 0
    for i in range(0, len(package_list)):
        print '#!!! %s'%package_list[i]
        xh = xh + 1
        path = REDE_PATH+package_list[i]+'\\'
      #  if '58' in package_list[i]: continue
      #  if '80' in package_list[i]: break
        tot = tot+1
        f_res = open(path+'process_results.txt')
        r = f_res.readline()
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        inside_list = os.listdir(path)
        apk_name = ""
        dex_path = ""
        if res['dex2jar'] == 1:
            for name in inside_list:
                if name[-4:] == '.apk' and 'dex2jar' in name:
                    apk_name = name
                    dex_path = path + 'dex2jar\\'

        else:
            for name in inside_list:
                if name[-4:] == '.apk' and 'enjarify' in name:
                    apk_name = name
                    dex_path = path + 'enjarify\\'

        apk_path = path + apk_name

        inside_file_list = os.listdir(path+'uncompress')
        dex_list = []
        for file in inside_file_list:
            if file[-4:] == '.dex':
                dex_list.append(file)
        if len(dex_list) == 1:
            if 'enjarify' in dex_path:
                jar_path = dex_path+'classes-enjarify.jar'
                out_jar_path = dex_path + 'classes-enjarify_out.jar'

            elif 'dex2jar' in dex_path:
                jar_path = dex_path+'classes-dex2jar.jar'
                out_jar_path = dex_path +'classes-dex2jar_out.jar'
        else:
            jar_path = dex_path + 'classes_merge.jar'
            out_jar_path = dex_path + 'classes_merge_out.jar'
        saveTable = {}
        saveTable['packageName'] = package_list[i]
        saveTable['before'] = os.path.getsize(jar_path)
        saveTable['after'] = os.path.getsize(out_jar_path)
        saveTable['num'] =  xh
        print json.dumps(saveTable,ensure_ascii=False)
        fsave.write(json.dumps(saveTable,ensure_ascii=False)+'\n')
        #break
    print tot

def show_shrink(X):
    #X = []
    Y = []

    for i in range(0,len(X)):
        Y.append(1.0/54.0)

    X = sorted(X)
    print X
    print Y

    plt.figure(figsize=(9, 6.5))
    YY = np.cumsum(Y)
    plt.xlabel('Code Reduction Size (MB)', fontsize=18)
    plt.ylabel('CDF', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    #plt.title('Distribution of Code Re=',fontsize=18)
    plt.plot(X, YY,marker='d',linewidth=1,color='c')
    plt.show()


if __name__ == '__main__':
    #cal_all()


    f = open('G:\PROGUARD_WORK_SPACE\TOP100_TEST//size_sta.txt','rb')
    y2 = []
    y3 = []
    d = []
    while True:
        r = f.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
      #  y2.append(float(res['before'])/(1024*1024.0))
      #  y3.append(float(res['after'])/(1024*1024.0))
        d.append((float(res['before'])/(1024*1024.0),float(res['after'])/(1024*1024.0)))
    import matplotlib.pyplot as plt

    print d
    ll = sorted(d)
    print ll
    x = range(0, 54)
    diff = []
    for i in ll:
        y2.append(i[0])
        y3.append(i[1])
        diff.append(abs(i[0]-i[1]))
    print diff
    show_shrink(diff)
    #y1 = [3, 6, 6, 8, 9]
    #y2 = [2, 5, 5, 7, 8]
   # y3 = [6, 6, 8, 8, 1]
    # p1 = plt.scatter(x, y1, marker='x', color='g', label='1', s=30)
    """
    p2 = plt.scatter(x, y2, marker='+', color='r', label='init size', s=30)
    p3 = plt.scatter(x, y3, marker='*', color='c', label='size after shrinking', s=30)
    plt.xticks([0,5,10,15,20,25,30,35,40,45,50,55],[0,5,10,15,20,25,30,35,40,45,50,55])
    #plt.title('Scatter')
    plt.grid(linestyle = "-.", color = "#CDC5BF", linewidth = 0.5)
    plt.legend(loc='lower right')
  #  plt.xticks(x)
    plt.xlabel('Order Number')
    plt.ylabel('Code Size (MB)')
    plt.show()
    """
