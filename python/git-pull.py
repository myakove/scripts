#!/usr/bin/python

from subprocess import PIPE
import subprocess
import os
import argparse
import my_functions

user_input = argparse.ArgumentParser()
user_input.add_argument('--git', '-G', help="path to git folder")
user_input.add_argument("--repo", "-R", help="Repo folder to update, use " +
                        "'folder1 folder2' for multipale folders")

option = user_input.parse_args()

if not (option.git and option.repo):
    print "Git path and repo folder must be specify"
    print user_input.format_usage()

else:
    git_repos = option.repo.split()
    git_folders = subprocess.Popen(["ls", option.git], stdout=PIPE,
                                   stderr=PIPE).communicate()[0].split()
    rc, repo_list = my_functions.FindInList(option.git, git_repos, git_folders)
    if rc == 0:
        for val in repo_list:
            os.chdir(option.git + "/" + val)
            print "\033[0;32m" + os.getcwd().split('/')[4] + "\033[0m"
            os.system("git checkout master")
            os.system("git pull")

