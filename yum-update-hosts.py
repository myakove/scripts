#! /usr/bin/python

from subprocess import call
import subprocess

processes = set()
max_processes = 20

#hosts=["red-vds2", "red-vds4", "orange-vdsc", "orange-vdsd", "silver-vdsa", "silver-vdsb", "blond-vdse","blond-vdsh", "orchid-vds1", "orchid-vds2", "navy-vds3", "camel-vdsa", "navy-vds1", "zeus-vds1",  "pink-vds3", "pink-vds2", "pink-vds4", "red-vds1", "red-vds3","blond-vdsd"]
hosts=["red-vds2", "red-vds4", "orange-vdsd", "blond-vdse","blond-vdsh", "navy-vds3", "camel-vdsa", "navy-vds1", "pink-vds2"]
domain = ".qa.lab.tlv.redhat.com"
user = "root"

def yumUpdate(host):
    processes.add(subprocess.Popen(["ssh", user + "@" + host + domain, "yum update -y > /dev/null"]))

for val in hosts:
    yumUpdate(val)
