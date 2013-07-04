#! /usr/bin/python

from my_functions import autoSSH
import multiprocessing
import argparse
import time

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--host", "-H", help="Host to connect to (host name " +
                        "if using range host name is without the number)")
USER_INPUT.add_argument("--domain", "-D", help="Domain for the host")
USER_INPUT.add_argument("--range", "-R", help="To run on range of hosts, " +
                        "example: 1-10 or 01-10")
USER_INPUT.add_argument("--username", "-U", default="root", help="user to " +
                        "connect to the host")
USER_INPUT.add_argument("--password", "-P", help="password to connect to " +
                        "the host", required=True)
USER_INPUT.add_argument("--file", "-F", help="File with hosts list, " +
                        "one host per line, don't use host, domain and " +
                        "range when using --file option")
USER_INPUT.add_argument("--connect", "-C", help="configure auto ssh to one " +
                        "host and connect to it", nargs='?', const=True)
OPTION = USER_INPUT.parse_args()


def sshHostRange(username, password, host, domain, host_range=list()):
    '''
    Get host range and run autoSSH function
    '''
    range_jobs = []
    for i in range(int(host_range[0]), int(host_range[1]) + 1):
        if '0' in (host_range[0] and host_range[1]):
            if i >= 10:
                idx = i
            else:
                idx = "0%d" % i
        active_host = "".join([host, str(idx), ".", domain])
        process = multiprocessing.Process(target=autoSSH,
                                          args=(active_host,
                                          username,
                                          password))
        range_jobs.append(process)
        process.start()
        time.sleep(1)

    for j in range_jobs:
        j.join()


def validateArgumantsAndRun():
    '''
    Validate syntax
    '''
    if OPTION.file:
        if (OPTION.host or OPTION.domain or OPTION.range):
            print "file can only be sent with --user and --password"
            USER_INPUT.print_help()
            return False

        else:
            hosts_file = open(OPTION.file, "r").readlines()
            jobs = []
            for host in hosts_file:
                ssh_host = host.strip()
                process = multiprocessing.Process(target=autoSSH,
                                                  args=(ssh_host,
                                                  OPTION.username,
                                                  OPTION.password))
                jobs.append(process)
                process.start()
                time.sleep(1)

            for j in jobs:
                j.join()

            return True

    if not OPTION.host:
        print "Host or connect must be specify"
        USER_INPUT.print_help()
        return False

    if OPTION.range:
        host_range = OPTION.range.split("-")
        sshHostRange(OPTION.username,
                     OPTION.password,
                     OPTION.host,
                     OPTION.domain,
                     host_range,)
        return True

    if OPTION.host:
        autoSSH(OPTION.host,
                OPTION.username,
                OPTION.password,
                OPTION.connect)
        return True

validateArgumantsAndRun()
