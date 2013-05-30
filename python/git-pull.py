#!/usr/bin/python

from subprocess import PIPE
import subprocess
import os
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument('--git', '-G', help="path to git folder")
option = user_input.parse_args()

if not option.git:
    print "Git path must be specify"
    print user_input.format_usage()

else:
    git_folders = subprocess.Popen(["ls", option.git], stdout=PIPE,
                                   stderr=PIPE).communicate()[0].split()
    for val in git_folders:
        os.chdir(option.git + val)
        print "\033[0;32m" + os.getcwd().split('/')[4] + "\033[0m"
        os.system("git pull")
