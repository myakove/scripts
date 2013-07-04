#! /bin/python

from my_functions import ldapSearch
import argparse

USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--user", "-U", help="User to sarch for.",
                        required=True)
OPTION = USER_INPUT.parse_args()

ldapSearch(OPTION.user)
