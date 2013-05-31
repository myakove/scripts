#! /usr/bin/python

import re
import os
import user
from subprocess import Popen, PIPE
from commands import getoutput


def autoSSH(host):
    '''
    Description: Get remote host ssh key and add it to local know_hosts file
    ssh-copy-id to remote host to enable ssh connect without password
    host = host to connect to
    '''
    home = user.home
    ssh_dir = ".ssh"
    ssh_file = "known_hosts"
    ssh_path = home + '/' + ssh_dir + '/' + ssh_file
    know_host = open(ssh_path, "r")

    for line in file.readlines(know_host):
        host_ip = Popen(["host", host], stdout=PIPE)
        out_host_ip, err_host_ip = host_ip.communicate()
        host_ip_addr = out_host_ip.split()
        if re.search(host, line):
            Popen(["ssh-keygen", "-R", host], stdout=PIPE)
        if re.search(host_ip_addr[3], line):
            Popen(["ssh-keygen", "-R", host_ip_addr[3]], stdout=PIPE)

    host_key = Popen(["ssh-keyscan", "-T", "5", host], stdout=PIPE)
    host_key_out, host_key_err = host_key.communicate()

    if host_key_err:
        print "\033[0;33m" + "No ssh keys from %s" % host + "\033[0m"
        return False

    if host_key_out:
        echo_cmd = 'echo " ' + host_key_out + '" >> ' + ssh_path
        Popen([echo_cmd], stdout=PIPE, shell=True)

    host_key_copy_err = Popen(["sshpass", "-p", "qum5net", "ssh-copy-id",
                               "root@" + host], stdout=PIPE).communicate()[1]

    if host_key_copy_err:
        print "\033[0;32m" + "Couldn't connect to %s" % host + "\033[0m"
    return True


def hostAlive(host):
    '''
    Description: Check if remote host is alive using ssh
    host = host to connect to
    '''
    if os.system("ssh -o ConnectTimeout=5 root@" + host + " exit &> /dev/null"):
        return True


def updateRepoAndInstall(version, hosts_file):
    '''
    Description: Update rhevm.repo to desire build and update the hosts
    version = build version to update to.
    hosts_file = file with hosts to update, one host per line.
    '''
    user = "root"
    repo_dir = "/etc/yum.repos.d/"
    tmp_file = "/tmp/rhevm.repo"
    host_list = open(hosts_file, "r")
    host_target_list = [line.strip() for line in host_list]
    host_target = ",".join(host_target_list)

    repo_file = open(tmp_file, "w")
    repo_file.write("[rhevm]" + "\n")
    repo_file.write("name=RHEVM" + "\n")
    repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" +
                    version + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.write("enable=1" + "\n")
    repo_file.close()

    for host in host_target_list:
        if os.system("pdsh -w " + host + " rpm -q pdsh"):
            os.system("pdsh -w " + host + " -l root yum install pdsh -y")
    os.system("pdcp -w " + host_target + " -l " + user + " " + tmp_file + " " +
              repo_dir)
    os.system("pdsh -w '^'" + hosts_file + " -l root yum clean all")
    os.system("pdsh -w '^'" + hosts_file + " -l root yum update -y")


def getMacAndIP(interface, host):
    '''
    Description: Get IP and MAC address from given host
    interface = Name of the interface to query
    host = Host to query
    '''
    mac = Popen((["ssh -o ConnectTimeout=5 root@" + host + " ifconfig " +
                  interface +
                  " | grep HWaddr |awk '{print $5}'"]), shell=True,
                stdout=PIPE)
    macout, macerr = mac.communicate()
    ip = Popen((["ssh -o ConnectTimeout=5 root@" + host + " ifconfig " +
                 interface + " | grep 'inet addr' |cut -d':' -f2|awk \
                 '{print $1}'"]), shell=True, stdout=PIPE)
    ipout, iperr = ip.communicate()
    return macout, ipout


def apkRename(apk_path, apk):
    '''
    Description: Rename apk to valid name.
    apk = apk file to rename
    '''
    cmd = Popen(("aapt  d  badging " + apk),
                shell=True,
                stdin=PIPE, stdout=PIPE, close_fds=True)
    fdin, fdout = cmd.stdin, cmd.stdout

    data = fdout.readlines()
    for line in data:
        if "application: label=" in line:
            apkname = line.split("'")[1]
        if "pack" in line:
            apkver = line.split("'")[5]

    newapkname = str(apkname) + "-" + str(apkver) + ".apk"
    newapkpath = apk_path[:-1]
    newapkpath.append(newapkname)
    newapkpathandname = '/'.join(newapkpath)
    os.system("mv " + apk + " " + newapkpathandname)


def ldapSearch(name):
    '''
    Description: Search for user in Redhat corp ldap server
    user = User to search for.
    '''
    search_string_uid = 'ldapsearch -x uid=*' + name + '*'
    search_string_cn = 'ldapsearch -x cn=*' + name + '*'

    result = getoutput(search_string_uid)
    if result.find('uid:') == -1:
        result = getoutput(search_string_cn)
        if result.find('cn:') == -1:
            print "\033[01;41m" + 'User not found' + "\033[0m"

    split_result = result.split('\n')

    param_dict = {'dn:': 'dn', 'cn:': 'Full Name:      ', 'uid:': 'IRC:       \
     ', 'mail:': 'Email:          ', 'telephoneNumber:':
                  'Office Ext:     ', 'mobile:': 'Mobile Phone:   ',
                  'rhatLocation:': 'Office Location:', 'rhatCostCenterDesc:':
                  'Job Title:      '}

    for line in split_result:
        for key in param_dict.keys():
            if line.startswith(key):
                if key == 'dn:':
                    print '\n'
                else:
                    print line.replace(key, "\033[01;10m" + param_dict[key] +
                                       "\033[0m")
    print '\n'


def IsServiceRunnig(service):
    '''
    Description: Check if service is running, retur PID of the service.
    service = service to search for.
    '''
    cmd = Popen(["pgrep", service], stdout=PIPE)
    out, err = cmd.communicate()
    list_out = out.split("\n")
    if out:
        print "Service %s is running" % (service)
        print "PID: %s" % (list_out[:-1])
        return
    return False


def OpenvpnConnect(username, password, conf_file):
    '''
    Description: Connect to openvpn server
    username = User to connect with
    password = Password to connect with
    conf_file = Configuration file to use
    '''
    pass_file = "/tmp/.vpn"
    tmp_file = open(pass_file, "w")
    tmp_file.write(username + "\n")
    tmp_file.write(password + "\n")
    tmp_file.close()
    openvpn = Popen(["sudo", "openvpn", "--config", conf_file,
                     "--auth-user-pass", pass_file], stdout=PIPE)
    out, err = openvpn.communicate()
    clean_tmp_file = Popen(["rm", "-rf", pass_file], stdout=None)
    if IsServiceRunnig is False:
        print "Failed to connect to VPN server"
        return False
    print "Connected to VPN"
    return True



