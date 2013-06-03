#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument("--hosts_file", "-H", help="hosts file, one host per line")
user_input.add_argument("--command", "-C", help="Command to run on remote hosts")
user_input.add_argument("--user", "-U", help="User for remote hosts connections (ssh)")
option = user_input.parse_args()

if not option.hosts_file:
    print "hosts file must be specify"
    print user_input.format_usage()

else:
    my_functions.ActionOnRemoteHosts(option.user, option.hosts_file, option.command)