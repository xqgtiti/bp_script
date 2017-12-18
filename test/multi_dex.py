
import sys
from dex_process.multi_dex import *
import pypinyin
test_apk_name = 'douban5.14.0.apk'
def test_multi_repack(test_apk_name, num):
    multi_repack(test_apk_name, num)

def test_multi_dex(test_apk_name,num):
    multi_dex(test_apk_name,num)

if __name__ == '__main__':
    #test_multi_dex(test_apk_name,3)
   # test_multi_repack(test_apk_name,3)