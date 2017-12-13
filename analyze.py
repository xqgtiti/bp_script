#import requests
import sys
sys.path.append('C:\Users//xqg//androguard//androguard')
print sys.path
import os
#print os.path.abspath(__file__)
#print sys.path
#import nump
from androguard.core.bytecodes import apk

if __name__ == '__main__':
    a = apk.APK('C:\Users//xqg//Desktop\single_class//google_play//com.jonathanrobins.pepe_snap.apk')
    print a.get_main_activity()
  #  all_activities =  a.get_activities()
  #  for i in all_activities:
  #      print i
