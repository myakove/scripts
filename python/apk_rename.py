#! /usr/bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--path', '-P', help="path to the APK file")
USER_INPUT.add_argument('--file', '-F', help="APK file to rename")
OPTION = USER_INPUT.parse_args()

if not (OPTION.path and OPTION.file):
    print "Path and APK file must be specify"
    print USER_INPUT.format_usage()

else:
    APK_PATH = OPTION.path.split('/')
    APK = OPTION.file

    my_functions.apkRename(APK_PATH, APK)
