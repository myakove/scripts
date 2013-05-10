#! /usr/bin/python

import my_functions
import user

home = user.home
dir = "pdsh-files"
hosts_file = "all-network-hosts"
hosts_list = open(home + "/" + dir + "/" + hosts_file, "r")
hosts = [line.strip() for line in hosts_list]


for host in hosts_list:
    if not my_functions.hostAlive(host):
        print "%s is alive" % host
    else:
        print "%s is down" % host
