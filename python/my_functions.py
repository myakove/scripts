#! /usr/bin/python

import re
import os
import user
import subprocess


def autoSSH(host):
    '''
    Description: Get remote host ssh key and add it to local know_hosts file
    ssh-copy-id to remote host to enable ssh connect without password
    host = host to connect to
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
    Description: Check if remote host is alive using ssh
    host = host to connect to
    '''
    if os.system("ssh -o ConnectTimeout=5 root@" + host + " exit &> /dev/null"):
        return True


def updateRepoAndInstall(version, hosts_file):
    '''
    Description: Update rhevm.repo to desire build and update the hosts
    version = build version to update to.
    hosts_file = file with hosts to update, one host per line.
    '''
    user = "root"
    repo_dir = "/etc/yum.repos.d/"
    tmp_file = "/tmp/rhevm.repo"
    host_list = open(hosts_file, "r")
    host_target_list = [line.strip() for line in host_list]
    host_target = ",".join(host_target_list)

    repo_file = open(tmp_file, "w")
    repo_file.write("[rhevm]" + "\n")
    repo_file.write("name=RHEVM" + "\n")
    repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" +
                    version + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.write("enable=1" + "\n")
    repo_file.close()

    for host in host_target_list:
        if not os.system("pdsh -w " + host + " rpm -q pdsh"):
            os.system("pdsh -w " + host + " -l root yum install pdsh -y")
    os.system("pdcp -w " + host_target + " -l " + user + " " + tmp_file + " " +
              repo_dir)
    os.system("pdsh -w '^'" + hosts_file + " -l root yum clean all")
    os.system("pdsh -w '^'" + hosts_file + " -l root yum update -y")
