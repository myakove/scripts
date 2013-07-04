#! /bin/python

from my_functions import getMacAndIP, COLORS
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument('--interface', '-I', help="Interface to query",
                        required=True)
USER_INPUT.add_argument('--host_file', '-H', help="File with hosts list, " +
                        "one host per line", required=True)
OPTION = USER_INPUT.parse_args()

HOSTS_FILE = open(OPTION.host_file, "r").readlines()

for host in HOSTS_FILE:
    active_host = host.strip()
    macout, ipout = getMacAndIP(OPTION.interface, active_host)
    print COLORS["brown"] + active_host, ":", COLORS["clear"]
    print "MAC address:", COLORS["green"], macout, COLORS["clear"]
    print "IP address :", COLORS["green"], ipout, COLORS["clear"]


