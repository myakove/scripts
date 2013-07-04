#! /usr/bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--path', '-P', help="path to the APK file",
                        required=True)
USER_INPUT.add_argument('--file', '-F', help="APK file to rename",
                        required=True)
OPTION = USER_INPUT.parse_args()

APK_PATH = OPTION.path.split('/')
APK = OPTION.file

my_functions.apkRename(APK_PATH, APK)
