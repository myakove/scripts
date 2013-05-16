#! /usr/bin/python

import my_functions
import sys

apk_path = sys.argv[1].split('/')
apk = sys.argv[1]

my_functions.apkRename(apk_path, apk)
