# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
import selenium
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
def get_google_play_top_list():
    driver = webdriver.Chrome()
    driver.get('https://play.google.com/store/apps/collection/topselling_free')

    cnt = 0

    package_name_list = []
    offset = 0
    while cnt < 300:
        top_list = driver.find_elements_by_css_selector("[class='card no-rationale square-cover apps small']")
        print len(top_list)
        for i in range(offset, offset + 60):
            print offset, offset+60
            cnt = cnt + 1
            print cnt
            print top_list[i].get_attribute('data-docid')
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
        print e.message
        print 'button not found'

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



def get_apk_by_apkpure(package_name):

    driver = webdriver.Chrome()
    driver.get('https://apkpure.com/search?q=%s'%package_name)
    apk_items = driver.find_elements_by_id('search-res')
    first_apk = apk_items[0]
    dt = first_apk.find_element_by_tag_name('dt')
    dt_a = dt.find_element_by_tag_name('a')
    apk_href = dt_a.get_attribute('href')
    download_apk_href = apk_href + '/download?from=details'
    driver.get(download_apk_href)

if __name__ == '__main__':

   get_google_play_top_list()


   # get_apk_by_apkpure('com.lenovo.anyshare.gps')
