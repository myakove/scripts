#! /usr/bin/python

import os
import sys

ver_input = sys.argv[1]
host_file_input = sys.argv[2]

hosts_path = host_file_input
user = "root"
repo_dir = "/etc/yum.repos.d/"
tmp_file = "/tmp/rhevm.repo"
host_list = open(host_file_input, "r")
host_target_list = [line.strip() for line in host_list]
host_target = ",".join(host_target_list)
print host_list
print host_target
print hosts_path


def updateRepo():
    repo_file = open(tmp_file, "w")
    repo_file.write("[rhevm]" + "\n")
    repo_file.write("name=RHEVM" + "\n")
    repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" +
                    ver_input + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.write("enable=1" + "\n")
    repo_file.close()
    os.system("pdcp -w " + host_target + " -l " + user + " " + tmp_file + " " +
              repo_dir)


def updateHosts():
    os.system("pdsh -w '^'" + hosts_path + " -l root yum update -y")

updateRepo()
updateHosts()




