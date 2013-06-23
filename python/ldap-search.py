#! /bin/python

import my_functions
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--user", "-U", help="User to sarch for.")
OPTION = USER_INPUT.parse_args()

if not OPTION.user:
    print "User must be specify"
    print USER_INPUT.format_usage()

else:
    my_functions.ldapSearch(OPTION.user)
