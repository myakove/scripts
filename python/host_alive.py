#! /usr/bin/python

from my_functions import hostAlive
from my_functions import COLORS
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--host", "-H", help="File with hosts list, one " +
                        "host per line", required=True)
OPTION = USER_INPUT.parse_args()

HOSTS_LIST = open(OPTION.host, "r")
HOSTS = [line.strip() for line in HOSTS_LIST]

for host in HOSTS:
    if hostAlive(host):
        OUTPUT = "".join([COLORS["brown"], "%s", COLORS["clear"], " is ",
                          COLORS["red"], "DOWN", COLORS["clear"]]) % host
        print OUTPUT
    else:
        OUTPUT = "".join([COLORS["brown"], "%s", COLORS["clear"], " is ",
                          COLORS["green"], "UP", COLORS["clear"]]) % host
        print OUTPUT
