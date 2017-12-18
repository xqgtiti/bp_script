# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
import selenium
import time
if __name__ == '__main__':

    driver = webdriver.Chrome()
    driver.get('https://apkpure.com/search?q=com.lenovo.anyshare.gps')
    apk_items = driver.find_elements_by_id('search-res')
    first_apk = apk_items[0]
    dt = first_apk.find_element_by_tag_name('dt')
    dt_a = dt.find_element_by_tag_name('a')
    apk_href = dt_a.get_attribute('href')
    download_apk_href = apk_href + '/download?from=details'
    driver.get(download_apk_href)

    driver.quit()