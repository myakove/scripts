#! /bin/python

import my_functions
import argparse

user_input = argparse.ArgumentParser()
user_input.add_argument("--user", "-U", help="User to sarch for.")
option = user_input.parse_args()
user = option.user

if not option.user:
    print "User must be specify"
    print user_input.format_usage()

else:
    my_functions.ldapSearch(user)