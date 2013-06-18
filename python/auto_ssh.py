#! /usr/bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument("--host", "-H", help="Host to connect to (host name " +
                        "without domain, if using range host name is " +
                        "without the number)")
user_input.add_argument("--domain", "-D", default="qa.lab.tlv.redhat.com",
                        help="Domain for the host")
user_input.add_argument("--range", "-R", help="To run on range of hosts, " +
                        "example: 1-10 or 01-10")
user_input.add_argument("--username", "-U", default="root", help="user to " +
                        "connect to the host")
user_input.add_argument("--password", "-P", help="password to connect to " +
                        "the host")
user_input.add_argument("--file", "-F", help="File with hosts list, " +
                        "one host per line, don't use host, domain and " +
                        "range when using --file option")
option = user_input.parse_args()


def sshHostRange():
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
            cmd = my_functions.autoSSH(host, option.username, option.password)
            if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host
        else:
            host = option.user + "@" + option.host + str(i) + "." + \
                option.domain
            cmd = my_functions.autoSSH(host, option.username, option.password)
            if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host


def validateArgumantsAndRun():
    if not option.password:
        print "password must be specify"
        print user_input.format_usage()
        return False
    if option.file:
        if option.host:
            print "file can only be sent with --user"
            print user_input.format_usage()
            return False
        if option.domain:
            print "file can only be sent with --user"
            print user_input.format_usage()
            return False
        if option.range:
            print "file can only be sent with --user"
            print user_input.format_usage()
            return False
        else:
            hosts_file = open(option.host_file, "r")
            for host in file.readlines(hosts_file):
                cmd = my_functions.autoSSH(host, option.username,
                                           option.password)
                if not cmd:
                    print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                          "\033[0m" % host
            return True

    if not option.host:
        print "Host or file must be specify"
        print user_input.format_usage()
        return False

    if option.file:
        hosts_file = open(option.host_file, "r")
        for host in file.readlines(hosts_file):
            cmd = my_functions.autoSSH(host, option.username, option.password)
            if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host
        return True

    if option.range:
        sshHostRange()
        return True

    else:
        host = option.host
        cmd = my_functions.autoSSH(host, option.username, option.password)
        if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s" +\
                      "\033[0m" % host
                return False

validateArgumantsAndRun()
