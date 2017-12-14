
import sys
from dex_process.single_dex import *

test_apk_name = 'com.jonathanrobins.pepe_snap.apk'
def test_single_repack(test_apk_name):
    single_repack(test_apk_name)

def test_single_dex(test_apk_name):
    single_dex(test_apk_name)

if __name__ == '__main__':
    test_single_dex(test_apk_name)
    test_single_repack(test_apk_name)