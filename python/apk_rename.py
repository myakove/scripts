#! /usr/bin/python

#from __future__ import print_function
import os
from subprocess import Popen, PIPE
import sys

apkpath = sys.argv[1].split('/')

p = Popen(("aapt  d  badging " + sys.argv[1]),
          shell=True,
          stdin=PIPE, stdout=PIPE, close_fds=True)
fdin, fdout = p.stdin, p.stdout

data = fdout.readlines()
for line in data:
    if "application: label=" in line:
        apkname = line.split("'")[1]
    if "pack" in line:
        apkver = line.split("'")[5]

newapkname = str(apkname) + "-" + str(apkver) + ".apk"
newapkpath = apkpath[:-1]
newapkpath.append(newapkname)
newapkpathandname = '/'.join(newapkpath)

os.system("mv " + sys.argv[1] + " " + newapkpathandname)
