#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line")
option = user_input.parse_args()

if option.host_file is None:
    print "Hosts file must be specify"
    print user_input.format_usage()

else:
    hosts_file = open(option.hosts_file, "r")
    for host in file.readlines(hosts_file):
        my_functions.autoSSH(host)


