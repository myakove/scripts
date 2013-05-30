#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument('--version', '-V', help='version to update the hosts')
user_input.add_argument('--host_file', '-H', help="File with hosts list, one " +
                        "host per line")
option = user_input.parse_args()

if not (option.version and option.host_file):
    print "Version and hosts file must be specify"
    print user_input.format_usage()

else:
    my_functions.updateRepoAndInstall(option.version, option.host_file)
