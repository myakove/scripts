#! /usr/bin/python

import my_functions
import user

home = user.home
pdsh_dir = "pdsh-files"
hosts_file = "all-network-hosts"
hosts_list = open(home + "/" + pdsh_dir + "/" + hosts_file, "r")
hosts = [line.strip() for line in hosts_list]


for host in hosts:
    if my_functions.hostAlive(host):
        print "%s is down" % host
    else:
        print "%s is alive" % host
