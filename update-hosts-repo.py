#! /usr/bin/python

import os
import user

processes = set()
max_processes = 20

input = raw_input("\033[0;32m" + 'Build: ' + "\033[0m")
hosts_file = "network-hosts"
home = user.home
hosts_path = home + "/pdsh-files/" + hosts_file
host_list = open(hosts_path, "r")
host_target_list = [line.strip() for line in host_list]
host_target = ",".join(host_target_list)
repo_dir = "/etc/yum.repos.d/"
tmp_file = "/tmp/rhevm.repo"
domain = ".qa.lab.tlv.redhat.com"
user = "root"


def updateRepo():
	repo_file = open(tmp_file, "w")
	repo_file.write("[rhevm]" + "\n")
	repo_file.write("name=RHEVM" + "\n")
	repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" + input + "\n")
	repo_file.write("gpgcheck=0" + "\n")
	repo_file.write("enable=1" + "\n")
	repo_file.close()
	os.system("pdcp -w " + host_target + " -l " + user + " " + tmp_file + " " + repo_dir)

def updateHosts():
	os.system("pdsh -w '^'" + hosts_path + " -l root yum update -y")

updateRepo()
updateHosts()



