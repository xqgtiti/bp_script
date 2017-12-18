# -*- coding:utf-8 -*- -
import os
from global_path import *
import numpy as np
import matplotlib
import json
import matplotlib.pyplot as plt

def show_code():
    X = []
    Y = []
    f = open('G:\PROGUARD_WORK_SPACE//cal.txt')
    tot = 0
    while True:
        r = f.readline()
        if not r: break
        tot = tot + 1
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        X.append(float(res['code_p']))
        Y.append(1.0 / 62.0)

    X = sorted(X)
    print X
    print Y

    plt.figure(figsize=(9, 6.5))
    YY = np.cumsum(Y)
    plt.xlabel('Code Percentage In APK', fontsize=18)
    plt.ylabel('CDF', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Distribution of Code Percentage In APK', fontsize=18)
    plt.plot(X, YY, marker='d', linewidth=1)
    plt.show()
def show_shrink():
    X = []
    Y = []
    f = open('G:\PROGUARD_WORK_SPACE//cal.txt')
    tot = 0
    while True:
        r = f.readline()
        if not r: break
        tot = tot + 1
        r = r[:-1]
        r = r.strip('\r')
        res = eval(r)
        X.append(float(res['shrink_p']))
        Y.append(1.0 / 62.0)

    X = sorted(X)
    print X
    print Y

    plt.figure(figsize=(9, 6.5))
    YY = np.cumsum(Y)
    plt.xlabel('Code Percentage After Shrinking', fontsize=18)
    plt.ylabel('CDF', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title('Distribution of Code Percentage After Shrinking',fontsize=18)
    plt.plot(X, YY,marker='d',linewidth=1)
    plt.show()

def cal():
    fsave = open('G:\PROGUARD_WORK_SPACE//cal.txt', 'w')
    f = open(PROGUARD_WORK_SPACE_WIN + 'success.txt', 'rb')
    r = f.readline()
    table = {}
    apk_list = []
    while True:
        r = f.readline()
        if not r: break
        r = r[:-1]
        r = r.strip('\r')
        # print r
        table[r] = 1
        apk_list.append(r)
    cnt = 0
    for apk_name in apk_list:
        # print apk_name
        pre_total_dex_size = 0
        now_total_dex_size = 0
        list = os.listdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\apk_uncompress\\')
        total_size = 0

        for root, dirs, files in os.walk(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\apk_uncompress\\'):
            for file in files:
                total_size = total_size + os.path.getsize(os.path.join(root, file))
        for file in list:
            if 'classes' in file and '.dex' in file:
                pre_total_dex_size = pre_total_dex_size + os.path.getsize(
                    PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\apk_uncompress\\' + file)
        # print pre_total_dex_size

        list_new_dex = os.listdir(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\new_dex\\')
        for file in list_new_dex:
            now_total_dex_size = now_total_dex_size + os.path.getsize(
                PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\new_dex\\' + file)
        # print now_total_dex_size
        if (now_total_dex_size * 1.0 / (pre_total_dex_size * 1.0) * 100) < 1: continue
        cnt = cnt + 1
        print cnt
        print apk_name
        print '%.2lf' % (now_total_dex_size * 1.0 / (pre_total_dex_size * 1.0) * 100) + '%'

        apk_path = PROGUARD_WORK_SPACE_WIN + apk_name
        apk_pre_size = os.path.getsize(apk_path)
        # print apk_pre_size

        apk_now_size = os.path.getsize(PROGUARD_WORK_SPACE_WIN + 'dir_' + apk_name + '\\' + apk_name)
        # print apk_now_size
        # print '%.2lf' % (apk_now_size * 1.0 / (apk_pre_size * 1.0) * 100) + '%'
        # print ''
        # break

        print '代码在apk中占得比例：'
        print '%.2lf' % (pre_total_dex_size * 1.0 / (total_size * 1.0) * 100) + '%'
        print ''

        save_table = {}
        save_table['apk_name'] = apk_name
        save_table['code_p'] = '%.2lf' % (pre_total_dex_size * 1.0 / (total_size * 1.0) * 100)
        save_table['shrink_p'] = '%.2lf' % (now_total_dex_size * 1.0 / (pre_total_dex_size * 1.0) * 100)
        fsave.write(json.dumps(save_table,ensure_ascii=False)+'\n')
if __name__ == '__main__':
    #cal()
    show_shrink()
    show_code()