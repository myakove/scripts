#!/usr/bin/python

from subprocess import PIPE
import subprocess
import os

git = "/home/" + os.getlogin() + "/git/"
git_folders = subprocess.Popen(["ls", git], stdout=PIPE, stderr=PIPE).communicate()[0].split()


    
for val in git_folders:
    os.chdir(git + val)
    print "\033[0;32m" + os.getcwd().split('/')[4] + "\033[0m"
    git_branch = subprocess.Popen(["git", "branch"], stdout=PIPE, stderr=PIPE).communicate()[0].split()
    for line in git_branch:
        os.system("git checkout " + line)
        os.system("git pull --rebase origin master")
    os.system("git checkout master")
    