#!/usr/bin/python

from subprocess import Popen, PIPE
import os
import argparse
import my_functions

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--git_folder', '-G', help="path to git folder")
USER_INPUT.add_argument("--repo", "-R", help="Repo folder to update, use " +
                        "'folder1 folder2' for multipale folders")

OPTION = USER_INPUT.parse_args()

if not (OPTION.git_folder and OPTION.repo):
    print "Git folder and repo folder must be specify"
    print USER_INPUT.format_usage()

else:
    GIT_REPOS = OPTION.repo.split()
    GIT_FOLDERS = Popen(["ls", OPTION.git_folder], stdout=PIPE,
                        stderr=PIPE).communicate()[0].split()
    RC, REPO_LIST = my_functions.findInList(GIT_REPOS, GIT_FOLDERS)
    if RC == 0:
        for val in REPO_LIST:
            os.chdir(OPTION.git_folder + "/" + val)
            print "\033[0;32m" + val + "\033[0m"
            os.system("git checkout master")
            os.system("git pull")

