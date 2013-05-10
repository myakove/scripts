#! /usr/bin/python

import os


def hostAlive():
    hosts_list_org = open("/home/myakove/pdsh-files/all-network-hosts", "r")
    hosts_list = [line.strip() for line in hosts_list_org]
    for host in hosts_list:
        if not os.system("ssh -o ConnectTimeout=5 root@" + host + " exit"):
            print "%s is alive" % host
        else:
            print "%s is down" % host
