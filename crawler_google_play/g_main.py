# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import selenium
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
from global_path import *


def get_google_play_top_list():
    driver = webdriver.Chrome()
    driver.get('https://play.google.com/store/apps/collection/topselling_free')

    cnt = 0

    package_name_list = []
    offset = 0
    while cnt < 300:
        top_list = driver.find_elements_by_css_selector("[class='card no-rationale square-cover apps small']")
        for i in range(offset, offset + 60):
            print (offset, offset+60)
            cnt = cnt + 1
            print (cnt)
            print (top_list[i].get_attribute('data-docid'))
            package_name_list.append(top_list[i].get_attribute('data-docid'))
            if cnt%60 == 0:
                actions = ActionChains(driver)
                actions.move_to_element(top_list[i])
                actions.perform()
                time.sleep(3)
        offset = offset + 60
    time.sleep(5)


    try:
        button = driver.find_element_by_id('show-more-button')
        button.click()
        time.sleep(3)
    except Exception as e:
        print (e.message)
        print ('button not found')

    while cnt < 540:
        top_list = driver.find_elements_by_css_selector("[class='card no-rationale square-cover apps small']")
        for i in range(offset, offset + 60):
            print offset
            cnt = cnt + 1
            print cnt
            print top_list[i].get_attribute('data-docid')
            package_name_list.append(top_list[i].get_attribute('data-docid'))
            if cnt % 60 == 0:
                actions = ActionChains(driver)
                actions.move_to_element(top_list[i])
                actions.perform()
                time.sleep(3)
        offset = offset + 60
    time.sleep(5)
    driver.quit()

    f = open('top540_package_name','w')
    rank = 0
    for package_name in package_name_list:
        rank = rank + 1
        save_table = {}
        save_table['package_name'] = package_name
        save_table['rank'] = rank

        f.write(json.dumps(save_table,ensure_ascii=False)+'\n')

    f.close()

def get_apk_by_apkpure(package_name, rank):
    options = webdriver.ChromeOptions()

    dir_apk_storage_path = APK_SOTRAGE_PATH + str(rank)+'_' + package_name
    if os.path.isdir(dir_apk_storage_path) == False:
        os.mkdir(dir_apk_storage_path)
    else:
        list = os.listdir(dir_apk_storage_path)
        if len(list) != 0 and list[0][-3:] == 'apk':
            print ('contiune!')
            return

    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': dir_apk_storage_path}
    options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://apkpure.com/search?q=%s'%package_name)
    apk_items = driver.find_elements_by_id('search-res')
    first_apk = apk_items[0]
    dt = first_apk.find_element_by_tag_name('dt')
    dt_a = dt.find_element_by_tag_name('a')
    apk_href = dt_a.get_attribute('href')
    download_apk_href = apk_href + '/download?from=details'
    driver.get(download_apk_href)

    pre_size = 0
    while True:
        list = os.listdir(dir_apk_storage_path)
        try:
            if list[0][-3:] == 'apk': break
        except: gd = 1

        try:

            if list[0][-10:] == 'crdownload':
                try:
                    now_size = os.path.getsize(dir_apk_storage_path+'\\'+list[0])
                    if now_size == pre_size: get_apk_by_apkpure(package_name,rank)
                    else: continue
                except: continue
        except: gd = 1
        time.sleep(2)
    print ('done!')
    driver.quit()

if __name__ == '__main__':

   #get_google_play_top_list

   #file_name = 'fsfsk.crdownload'
  # print file_name[-11:]



   f = open(GET_TOP_APK_PATH+'top540_package_name.txt')

   while True:
       r = f.readline()
       if not r: break
       r = r[:-1]
       r = r.strip('\r')
       res = eval(r)

       if (res['rank'] == 1 or res['rank'] == 87 or res['rank'] == 107 or res['rank'] == 175
       or res['rank'] == 179 or res['rank'] == 193 or res['rank'] == 244
       or res['rank'] == 291 or res['rank'] == 304 or res['rank'] == 370) :continue
       print (str(res['rank'])+': '+ res['package_name'])
       get_apk_by_apkpure(res['package_name'], res['rank'])