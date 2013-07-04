#! /usr/bin/python

import argparse
import my_functions

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--server", "-SRV", help="Jenkins server",
                        required=True)
USER_INPUT.add_argument("--username", "-U", help="Username for Jenkins server")
USER_INPUT.add_argument("--password", "-P", help="Password got Jenkins server")
USER_INPUT.add_argument("--action", "-A", help="action to run on the job,"
                        "enable, disable, print (name), delete, info, "
                        "is_queued and build", required=True)
USER_INPUT.add_argument("--search", "-S", help="search for job to apply the"
                        "action")
USER_INPUT.add_argument("--view", "-V", help="Jenkins view", required=True)
USER_INPUT.add_argument("--nview", "-NV", help="Nested Jenkins view",
                        required=True)
OPTION = USER_INPUT.parse_args()

my_functions.jenkinsCMD(OPTION.server, OPTION.action, OPTION.view,
                        OPTION.nview, username=OPTION.username,
                        password=OPTION.password, search=OPTION.search)
