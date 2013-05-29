#! /bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument('--interface', '-I', help="Interface to query")
user_input.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line")
option = user_input.parse_args()

if option.interface or option.host_file is None:
    print "Interface and hosts file must be specify"
    print user_input.format_usage()

else:
    hosts_tmp = open(option.host_file, "r").readlines()
    hosts_file = [line.strip() for line in hosts_tmp]

    for host in hosts_file:
        macout, ipout = my_functions.getMacAndIP(option.interface, host)
        print "\033[0;33m" + "%s :" % host + "\033[0m"
        print "MAC address: " + "\033[0;32m" + macout + "\033[0m"
        print "IP address : " + "\033[0;32m" + ipout + "\033[0m"

