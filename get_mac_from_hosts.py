#! /bin/python

from subprocess import call

user_input = raw_input("\033[0;32m" + 'Interface: ' + "\033[0m")
hosts=["red-vds2", "red-vds4", "orange-vdsc", "orange-vdsd", "silver-vdsa", "silver-vdsb", "blond-vdse","blond-vdsh", "orchid-vds1", "orchid-vds2", "navy-vds3", "camel-vdsa", "navy-vds1", "zeus-vds1",  "pink-vds3", "pink-vds2", "pink-vds4", "red-vds1", "red-vds3","blond-vdsd"]
domain = ".qa.lab.tlv.redhat.com"
user = "root"

def getMac( user, host, domain, interface ):
    print host + domain,  user_input,  "MAC and IP address is:"
    if call(["ssh", user + "@" + host + domain, "ifconfig", user_input, "| grep", user_input, "| awk '{print  $5}'"]) !=0:
        return
    call(["ssh", user + "@" + host + domain, "ifconfig", user_input, "| grep 'inet addr'|cut -d':' -f2|awk '{print $1}'"])
    print "\n"

for val in hosts:    
    getMac(user, val, domain, user_input)