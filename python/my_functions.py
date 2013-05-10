#! /usr/bin/python

import re
import os
import user


def autoSSH(host):
    '''
    host = host to connect to
    Get remote host ssh key and add it to local know_hosts file
    ssh-copy-id to remote host to enable ssh connect without password
    '''
    home = user.home
    ssh_dir = ".ssh"
    ssh_file = "known_hosts"
    ssh_path = home + '/' + ssh_dir + '/' + ssh_file
    know_host = open(ssh_path, "r")
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


def hostAlive(host):
    '''
    host = host to connect to
    Check if remote host is alive using ssh
    '''
    if not os.system("ssh -o ConnectTimeout=5 root@" + host + " exit"):
        print "%s is alive" % host
    else:
        print "%s is down" % host
