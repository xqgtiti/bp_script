from androguard.core.analysis.analysis import VMAnalysis
from androguard.core.bytecodes.apk import APK
from androguard.core.bytecodes.dvm import DalvikVMFormat
from core.analysis import *
if __name__ == '__main__':
    a = APK("1_1.apk")
    print len(a.get_activities())
    print a.get_main_activity()
    d = DalvikVMFormat(a.get_dex())
    dx = VMAnalysis(d)
    print dx.get_method_signature()