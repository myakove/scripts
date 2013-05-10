#! /usr/bin/python

from subprocess import call
import subprocess

processes = set()
max_processes = 20

input = raw_input("\033[0;32m" + 'Build: ' + "\033[0m")
hosts=["red-vds2", "red-vds4", "orange-vdsc", "orange-vdsd", "blond-vdse","blond-vdsh"]
location = ":/etc/yum.repos.d/"
repo = "/tmp/rhevm.repo"
domain = ".qa.lab.tlv.redhat.com"
user = "root"

def updateRepo( host ):
	repo_file = open("/tmp/rhevm.repo", "w")
	repo_file.write("[rhevm]" + "\n")
	repo_file.write("name=RHEVM" + "\n")
	repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" + input + "\n")
	repo_file.write("gpgcheck=0" + "\n")
	repo_file.write("enable=1" + "\n")
	repo_file.close()
	processes.add(subprocess.Popen(["scp", repo, user + "@" + host + domain + location]))

for val in hosts:
	updateRepo(val)
