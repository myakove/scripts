#! /usr/bin/python

import sys
import my_functions

version = sys.argv[1]
hosts_file = sys.argv[2]

my_functions.updateRepoAndInstall(version, hosts_file)
