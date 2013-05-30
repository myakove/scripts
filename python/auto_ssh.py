#! /usr/bin/python

import my_functions
import optparse
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument("--host", "-H", help="Host to connect to (host name " +
                        "without domain, if using range host name is without " +
                        "the number)")
user_input.add_argument("--domain", "-D", default="qa.lab.tlv.redhat.com",
                        help="Domain for the host")
user_input.add_argument("--range", "-R", help="To run on range of hosts, " +
                        "example: 1-10")
user_input.add_argument("--user", "-U", default="root", help="user to " +
                        "connect to the host")
option = user_input.parse_args()


def host_range():
    flag_zero = False
    if option.range[0] == "0":
        flag_zero = True
    host_range = option.range.split("-")
    start_range = int(host_range[0])
    end_range = int(host_range[1])
    for i in range(start_range, end_range + 1):
        if flag_zero and i < 10:
            i = '0' + str(i)
            host = option.user + "@" + option.host + str(i) + "." + \
                option.domain
            cmd = my_functions.autoSSH(host)
            if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host
        else:
            host = option.user + "@" + option.host + str(i) + "." + \
                option.domain
            cmd = my_functions.autoSSH(host)
            if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host

if not option.host:
    print "Host must be specify"
    print user_input.format_usage()

elif option.range:
    host_range()

else:
    host = option.user + "@" + option.host + "." + option.domain
    cmd = my_functions.autoSSH(host)
