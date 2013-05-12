#! /usr/bin/python

import my_functions
import re

input = raw_input("\033[0;32m" + 'Hostname: ' + "\033[0m")


if re.search('range', input):
    params = input.split("|")[:-1]
    start_range = int(params[1])
    end_range = int(params[2])
    print params
    for i in range(start_range, end_range):
        if i < 10:
            i_str = '0' + str(i)
        host = params[0] + i_str + params[3]
        cmd = my_functions.autoSSH(host)
        if cmd:
            print "Fail to configure auto ssh to %s" % host

else:
    host = input
    cmd = my_functions.autoSSH(host)
    if cmd:
        print "Fail to configure auto ssh to %s" % host
