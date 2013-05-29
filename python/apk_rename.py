#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument('--path', '-P', help="path to the APK file")
user_input.add_argument('--file', '-F', help="APK file to rename")
option = user_input.parse_args()

if option.path or option.file is None:
    print "Path and APK file must be specify"
    print user_input.format_usage()

else:
    apk_path = option.path.split('/')
    apk = option.file

    my_functions.apkRename(apk_path, apk)
