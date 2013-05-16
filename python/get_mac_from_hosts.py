#! /bin/python

import my_functions
import sys

interface = sys.argv[1]
hosts = sys.argv[2]
hosts_tmp = open(hosts, "r").readlines()
hosts_file = [line.strip() for line in hosts_tmp]


for host in hosts_file:
    macout, ipout = my_functions.getMacAndIP(interface, host)
    print "\033[0;33m" + "%s :" % host + "\033[0m"
    print "MAC address: " + "\033[0;32m" + macout + "\033[0m"
    print "IP address : " + "\033[0;32m" + ipout + "\033[0m"
