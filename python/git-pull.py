#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import argparse
import my_functions

user_input = argparse.ArgumentParser()
user_input.add_argument('--git_folder', '-G', help="path to git folder")
user_input.add_argument("--repo", "-R", help="Repo folder to update, use " +
                        "'folder1 folder2' for multipale folders")

option = user_input.parse_args()

if not (option.git_folder and option.repo):
    print "Git folder and repo folder must be specify"
    print user_input.format_usage()

else:
    git_repos = option.repo.split()
    git_folders = Popen(["ls", option.git_folder], stdout=PIPE,
                        stderr=PIPE).communicate()[0].split()
    rc, repo_list = my_functions.findInList(git_repos, git_folders)
    if rc == 0:
        for val in repo_list:
            os.chdir(option.git_folder + "/" + val)
            print "\033[0;32m" + val + "\033[0m"
            os.system("git checkout master")
            os.system("git pull")

