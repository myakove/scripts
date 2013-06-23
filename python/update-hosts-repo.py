#! /usr/bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--version', '-V', help='version to update the hosts')
USER_INPUT.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line")
OPTION = USER_INPUT.parse_args()

if not (OPTION.version and OPTION.host_file):
    print "Version and hosts file must be specify"
    print USER_INPUT.format_usage()

else:
    my_functions.updateRepoAndInstall(OPTION.version, OPTION.host_file)
