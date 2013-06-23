#! /usr/bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--host", "-H", help="File with hosts list, one " +
                        "host per line")
OPTION = USER_INPUT.parse_args()

if not OPTION.host:
    print "Hosts file must be specify"
    print USER_INPUT.format_usage()

else:
    HOSTS_LIST = open(OPTION.host, "r")
    HOSTS = [line.strip() for line in HOSTS_LIST]

    for host in HOSTS:
        if my_functions.hostAlive(host):
            print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + \
                  "\033[0;31m" + "down" + "\033[0m"
        else:
            print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + \
                  "\033[0;32m" + "alive" + "\033[0m"

