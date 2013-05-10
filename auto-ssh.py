#! /usr/bin/python

import os
import re
import user

input = raw_input("\033[0;32m" + 'Hostname: ' + "\033[0m")
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


if re.search('range', input):
    params = input.split("|")[:-1]
    start_range = int(params[1])
    end_range = int(params[2])
    print params
    for i in range(start_range, end_range):
        if i < 10:
            i_str = '0' + str(i)
        host = params[0] + i_str + params[3]
        cmd = autoSSH(host)
        if cmd:
            print "Fail to configure auto ssh to %s" % host

else:
    host = input
    cmd = autoSSH(host)
    if cmd:
        print "Fail to configure auto ssh to %s" % host
