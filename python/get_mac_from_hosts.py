#! /bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--interface', '-I', help="Interface to query")
USER_INPUT.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line")
OPTION = USER_INPUT.parse_args()

if not (OPTION.interface and OPTION.host_file):
    print "Interface and hosts file must be specify"
    print USER_INPUT.format_usage()

else:
    HOSTS_TMP = open(OPTION.host_file, "r").readlines()
    HOSTS_FILE = [line.strip() for line in HOSTS_TMP]

    for host in HOSTS_FILE:
        macout, ipout = my_functions.getMacAndIP(OPTION.interface, host)
        print "\033[0;33m" + "%s :" % host + "\033[0m"
        print "MAC address: " + "\033[0;32m" + macout + "\033[0m"
        print "IP address : " + "\033[0;32m" + ipout + "\033[0m"

