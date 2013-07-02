#! /bin/python

from my_functions import getMacAndIP, COLORS
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--interface', '-I', help="Interface to query")
USER_INPUT.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line")
OPTION = USER_INPUT.parse_args()

if not (OPTION.interface and OPTION.host_file):
    print "Interface and hosts file must be specify"
    print USER_INPUT.format_usage()

else:
    HOSTS_FILE = open(OPTION.host_file, "r").readlines()

    for host in HOSTS_FILE:
        active_host = host.strip()
        macout, ipout = getMacAndIP(OPTION.interface, active_host)
        print COLORS["brown"] + active_host, ":", COLORS["clear"]
        print "MAC address:", COLORS["green"], macout, COLORS["clear"]
        print "IP address :", COLORS["green"], ipout, COLORS["clear"]


