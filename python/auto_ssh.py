#! /usr/bin/python

import my_functions
import multiprocessing
import argparse
import time

user_input = argparse.ArgumentParser()
user_input.add_argument("--host", "-H", help="Host to connect to (host name " +
                        "if using range host name is without the number)")
user_input.add_argument("--domain", "-D", help="Domain for the host")
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


def sshHostRange(username, password, host, domain, host_range=[]):
    range_jobs = []
    for i in range(int(host_range[0]), int(host_range[1]) + 1):
        if '0' in (host_range[0] and host_range[1]):
            if i >= 10:
                idx = i
            else:
                idx = "0%d" % i
        active_host = "".join([host, str(idx), ".", domain])
        process = multiprocessing.Process(target=my_functions.autoSSH,
                                          args=(active_host,
                                          username,
                                          password))
        range_jobs.append(process)
        process.start()
        time.sleep(1)

    for j in range_jobs:
        j.join()
        print "\033[0;32m", range_jobs, "\033[0m"


def validateArgumantsAndRun():
    if not option.password:
        print "password must be specify"
        print user_input.format_usage()
        return False

    if option.file:
        if (option.host or option.domain or option.range):
            print "file can only be sent with --user and --password"
            print user_input.format_usage()
            return False

        else:
            hosts_file = open(option.file, "r").readlines()
            jobs = []
            for host in hosts_file:
                ssh_host = host.strip()
                process = multiprocessing.Process(target=my_functions.autoSSH,
                                                  args=(ssh_host,
                                                  option.username,
                                                  option.password))
                jobs.append(process)
                process.start()
                time.sleep(1)

            for j in jobs:
                j.join()
                print "\033[0;32m", jobs, "\033[0m"
            return True

    if not option.host:
        print "Host or file must be specify"
        print user_input.format_usage()
        return False

    if option.range:
        host_range = option.range.split("-")
        sshHostRange(option.username,
                     option.password,
                     option.host,
                     option.domain,
                     host_range,)
        return True

    else:
        cmd = my_functions.autoSSH(option.host,
                                   option.username,
                                   option.password)
        if not cmd:
                print "\033[0;32m" + "Fail to configure auto ssh to %s"\
                      % option.host + "\033[0m"
                return False

validateArgumantsAndRun()
