#! /bin/python

from commands import getoutput

input = raw_input("\033[0;32m" + 'Search for Name/Username: ' + "\033[0m")
search_string_uid = 'ldapsearch -x uid=*' + input + '*'
search_string_cn = 'ldapsearch -x cn=*' + input + '*'

result = getoutput(search_string_uid)
if result.find('uid:') == -1:
    result = getoutput(search_string_cn)
    if result.find('cn:') == -1:
        print "\033[01;41m" + 'User not found' + "\033[0m"

split_result = result.split('\n')

param_dict = {'dn:' : 'dn', 'cn:' : 'Full Name:      ', 'uid:' : 'IRC:            ', 'mail:' : 'Email:          ', 'telephoneNumber:' : 'Office Ext:     ', 'mobile:' : 'Mobile Phone:   ', 'rhatLocation:' : 'Office Location:', 'rhatCostCenterDesc:' : 'Job Title:      '}

for line in split_result:
    for key in param_dict.keys():
        if line.startswith(key):
            if key == 'dn:':
                print '\n'
            else:
                print line.replace(key, "\033[01;10m" + param_dict[key] + "\033[0m")

print '\n'