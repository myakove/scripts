#! /usr/bin/python

import my_functions
import sys

pdsh_dir = "pdsh-files"
hosts_file = "all-network-hosts"
host_file_input = sys.argv[1]
hosts_list = open(host_file_input, "r")
hosts = [line.strip() for line in hosts_list]


for host in hosts:
    if my_functions.hostAlive(host):
        print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + "\033[0;31m" +\
              "down" + "\033[0m"
    else:
        print "\033[0;33m" + "%s " % host + "\033[0m" + "is " + "\033[0;32m" +\
              "alive" + "\033[0m"
