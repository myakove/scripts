#! /usr/bin/python

import my_functions
import sys

hosts_file = open(sys.argv[1], "r")

for host in file.readlines(hosts_file):
    my_functions.autoSSH(host)


