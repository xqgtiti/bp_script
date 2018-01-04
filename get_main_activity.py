from androguard.core.bytecodes import apk

a = apk.APK('G:\PROGUARD_WORK_SPACE\GET_TOP_APK\APK_STORAGE//5_com.google.android.apps.tachyon//test.apk', raw=False)
print a.get_main_activity()