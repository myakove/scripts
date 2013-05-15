#! /usr/bin/python

import re
import os
import user
import subprocess


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
        host_ip = subprocess.Popen(["host", host], stdout=subprocess.PIPE)
        out_host_ip, err_host_ip = host_ip.communicate()
        host_ip_addr = out_host_ip.split()
        if re.search(host, line):
            os.system("ssh-keygen -R " + host)
        if re.search(host_ip_addr[3], line):
            os.system("ssh-keygen -R " + host_ip_addr[3])
    if os.system("ssh-keyscan -T 5 " + host + " | grep -v '#' &>> " + ssh_path):
        print "\033[0;33m" + "No ssh keys from %s" % host + "\033[0m"
    if os.system("sshpass -p 'qum5net' ssh-copy-id root@" + host):
        print "\033[0;32m" + "Couldn't connect to %s" % host + "\033[0m"
    return True


def hostAlive(host):
    '''
    host = host to connect to
    Check if remote host is alive using ssh
    '''
    if os.system("ssh -o ConnectTimeout=5 root@" + host + " exit &> /dev/null"):
        return True
