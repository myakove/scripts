#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument("--host", "-H", help="File with hosts list, one " +
                        "host per line")
option = user_input.parse_args()

if not option.host:
    print "Hosts file must be specify"
    print user_input.format_usage()

else:
    hosts_list = open(option.host, "r")
    hosts = [line.strip() for line in hosts_list]

    for host in hosts:
        if my_functions.hostAlive(host):
            print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + \
                  "\033[0;31m" + "down" + "\033[0m"
        else:
            print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + \
                  "\033[0;32m" + "alive" + "\033[0m"

