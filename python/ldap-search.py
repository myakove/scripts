#! /bin/python

from my_functions import ldapSearch
import argparse
import ConfigParser
import user
import os

CONF_FILE = user.home + "/.ldap-search.conf"
USER_INPUT = argparse.ArgumentParser()
USER_INPUT.add_argument("--server", "-S", help="ldap server")
USER_INPUT.add_argument("--domain", "-D", help="domain of the ldap server")
USER_INPUT.add_argument("--user", "-U", help="User to sarch for.",
                        required=True)
USER_INPUT.add_argument("--file", "-F", help="conf file with server and " +
                        "domain. File should be at $HOME/.ldap-search.conf " +
                        "Example file:" +
                        "[SETTING]" +
                        "server=ldap.server" +
                        "domain=domain.com",
                        nargs='?', const=True)
OPTION = USER_INPUT.parse_args()


def validateInput():
    if not (OPTION.server and OPTION.domain):
        if OPTION.file:
            if not os.path.isfile(CONF_FILE):
                print CONF_FILE, "is missing"
                return False
            config = ConfigParser.RawConfigParser()
            config.read(CONF_FILE)
            server = config.get("SETTING", "server")
            domain = config.get("SETTING", "domain")
            ldapSearch(server, OPTION.user, domain)
            return True
        print "Server and domain or file must be specify"
        return False
    else:
        server = OPTION.server
        domain = OPTION.domain
        ldapSearch(server, OPTION.user, domain)
    return True

validateInput()
