#!/usr/bin/python

from subprocess import PIPE
import subprocess
import os
import argparse
import re

user_input = argparse.ArgumentParser()
user_input.add_argument('--git', '-G', help="path to git folder")
user_input.add_argument("--repo", "-R", help="Repo folder to update, use " +
                        "'folder1 folder2' for multipale folders")

option = user_input.parse_args()

'''
def findInList(list1, list2):
    for val in git_repos:
        status = 0
        if val not in git_folders:
            print "%s not found in %s folder" % (val, option.git)
            status = 1
    if status is 1:
        return False
    return True
'''
def findInList(list1, list2):
    repo_list = []
    status = 1
    for val in git_repos:
        if val in git_folders:
            repo_list.append(val)
            status = 0
        else:
            print "%s not found in %s folder" % (val, option.git)
    return status, repo_list





if not (option.git and option.repo):
    print "Git path and repo folder must be specify"
    print user_input.format_usage()

else:
    git_repos = option.repo.split()
    git_folders = subprocess.Popen(["ls", option.git], stdout=PIPE,
                                   stderr=PIPE).communicate()[0].split()
    rc, repo_list = findInList(git_folders, git_repos)
    if rc == 0:
        for val in repo_list:
            os.chdir(option.git + "/" + val)
            print "\033[0;32m" + os.getcwd().split('/')[4] + "\033[0m"
            os.system("git checkout master")
            os.system("git pull")

