#! /usr/bin/python

import re
import os
import user

home = user.home
ssh_dir = ".ssh"
ssh_file = "known_hosts"
ssh_path = home + '/' + ssh_dir + '/' + ssh_file


def autoSSH(host):
    know_host = open(ssh_path)
    for line in file.readlines(know_host):
        if re.search(host, line):
            os.system("ssh-keygen -R " + host)
    if os.system("ssh-keyscan -T 5 " + host + " | grep -v '#' &>> " + ssh_path):
        print "No ssh keys from %s" % host
        return False
    if os.system("sshpass -p 'qum5net' ssh-copy-id root@" + host):
        print "Couldn't connect to %s" % host
        return False
    return True


def hostAlive():
    hosts_list_org = open("/home/myakove/pdsh-files/all-network-hosts", "r")
    hosts_list = [line.strip() for line in hosts_list_org]
    for host in hosts_list:
        if not os.system("ssh -o ConnectTimeout=5 root@" + host + " exit"):
            print "%s is alive" % host
        else:
            print "%s is down" % host