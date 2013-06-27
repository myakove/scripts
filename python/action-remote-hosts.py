#! /usr/bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--hosts_file", "-H", help="hosts file, one host " +
                        "per line")
USER_INPUT.add_argument("--command", "-C", help="Command to run on remote " +
                        "hosts")
USER_INPUT.add_argument("--user", "-U", help="User for remote hosts " +
                        "connections (ssh, default is root)")
OPTION = USER_INPUT.parse_args()

if OPTION.user is None:
    OPTION.user = "root"

if not (OPTION.hosts_file and OPTION.command):
    print "hosts file and command must be specify"
    print USER_INPUT.format_usage()

else:
    OPTION.user = "root"
    my_functions.actionOnRemoteHosts(OPTION.hosts_file,
                                     OPTION.command,
                                     OPTION.user)
