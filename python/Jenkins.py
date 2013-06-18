#! /usr/bin/python

import argparse
import my_functions

user_input = argparse.ArgumentParser()
user_input.add_argument("--server", "-SRV", help="Jenkins server")
user_input.add_argument("--username", "-U", help="Username for Jenkins server")
user_input.add_argument("--password", "-P", help="Password got Jenkins server")
user_input.add_argument("--action", "-A", help="action to run on the job,"
                        "enable, disable, print (name), delete, info and "
                        "build")
user_input.add_argument("--search", "-S", help="search for job to apply the"
                        "action")
user_input.add_argument("--view", "-V", help="Jenkins view")
user_input.add_argument("--nview", "-NV", help="Nested Jenkins view")
option = user_input.parse_args()

if not (option.server and
        option.action and
        option.view and
        option.nview):
    print "Server, search, action, view and nview must be specify"
    print user_input.format_usage()

else:
    my_functions.jenkinsCMD(option.server, option.action, option.view,
                            option.nview, username=option.username,
                            password=option.password, search=option.search)
