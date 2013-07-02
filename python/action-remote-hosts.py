#! /usr/bin/python

from my_functions import actionOnRemoteHosts
import argparse
import multiprocessing

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--hosts_file", "-H", help="hosts file, one host " +
                        "per line", required=True)
USER_INPUT.add_argument("--command", "-C", help="Command to run on remote " +
                        "hosts", required=True)
USER_INPUT.add_argument("--user", "-U", help="User for remote hosts " +
                        "connections (ssh, default is root)", default="root")
OPTION = USER_INPUT.parse_args()

JOBS = []
HOSTS = open(OPTION.hosts_file, "r").readlines()
for host in HOSTS:
    ssh_host = host.strip()
    PROCESS = multiprocessing.Process(target=actionOnRemoteHosts,
                                      args=(ssh_host,
                                      OPTION.command, OPTION.user))
    JOBS.append(PROCESS)
    PROCESS.start()

for j in JOBS:
    j.join()

