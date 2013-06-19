#! /usr/bin/python

import re
import os
import user
import time
import logging
from subprocess import Popen, PIPE
from commands import getoutput


def autoSSH(host, username, password):
    '''
    Description: Get remote host ssh key and add it to local know_hosts file
    ssh-copy-id to remote host to enable ssh connect without password
    host = host to connect to format: user@host
    '''
    yb = True
    try:
        import yum
        yb = yum.YumBase().isPackageInstalled("sshpass")
    except ImportError:
        logging.info("If this script fails check if sshpass in installed")
        pass

    if not yb:
        print "sshpass is not installed"
        return False

    else:
        home = user.home
        ssh_dir = ".ssh"
        ssh_file = "known_hosts"
        ssh_path = home + '/' + ssh_dir + '/' + ssh_file
        know_host = open(ssh_path, "r").readlines()

        for line in know_host:
            host_ip = Popen(["host", host], stdout=PIPE).communicate()[0]
            host_ip_addr = host_ip.split()
            if host in line:
                Popen(["ssh-keygen", "-R", host], stdout=PIPE)
            if host_ip_addr[3] in line:
                Popen(["ssh-keygen", "-R", host_ip_addr[3]], stdout=PIPE)
            '''
            if re.search(host, line):
                Popen(["ssh-keygen", "-R", host], stdout=PIPE)
            if re.search(host_ip_addr[3], line):
                Popen(["ssh-keygen", "-R", host_ip_addr[3]], stdout=PIPE)
            '''
        host_key = Popen(["ssh-keyscan", "-T", "5", host], stdout=PIPE)
        host_key_out, host_key_err = host_key.communicate()

        if host_key_err:
            print "\033[0;33m" + "No ssh keys from %s" % host + "\033[0m"
            return False

        if host_key_out:
            echo_cmd = 'echo " ' + host_key_out + '" >> ' + ssh_path
            Popen([echo_cmd], stdout=PIPE, shell=True)

        host_key_copy_err = Popen(["sshpass", "-p", password, "ssh-copy-id",
                                   username + "@" + host],
                                  stdout=PIPE).communicate()[1]

        if host_key_copy_err:
            print "\033[0;32m" + "Couldn't connect to %s" % host + "\033[0m"
        return True


def hostAlive(host):
    '''
    Description: Check if remote host is alive using ssh
    host = host to connect to
    '''
    if os.system("ssh -o ConnectTimeout=5 root@" + host +
                 " exit &> /dev/null"):
        return True


def updateRepoAndInstall(version, hosts_file):
    '''
    Description: Update rhevm.repo to desire build and update the hosts
    version = build version to update to.
    hosts_file = file with hosts to update, one host per line.
    '''
    yb = True
    try:
        import yum
        yb = yum.YumBase().isPackageInstalled("sshpass")
    except ImportError:
        logging.info("If this script fails check if pdsh in installed")
        pass

    if not yb:
        print "pdsh is not installed"
        return False

    else:
        user = "root"
        repo_dir = "/etc/yum.repos.d/"
        tmp_file = "/tmp/rhevm.repo"
        host_list = open(hosts_file, "r")
        host_target_list = [line.strip() for line in host_list]

        repo_file = open(tmp_file, "w")
        repo_file.write("[rhevm]" + "\n")
        repo_file.write("name=RHEVM" + "\n")
        repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" +
                        version + "\n")
        repo_file.write("gpgcheck=0" + "\n")
        repo_file.write("enable=1" + "\n")
        repo_file.close()

        for host in host_target_list:
            cmd_scp = Popen(["scp", tmp_file, user + "@" + host + ":" +
                             repo_dir],
                            stdout=PIPE)
            out_scp, err_scp = cmd_scp.communicate()
            if err_scp:
                print "Failed to copy repo file to %s" % host
                return False

        cmd_clean = Popen(["pdsh", "-w", "^" + hosts_file, "-l", "root", "yum",
                           "clean", "all"], stdout=PIPE)
        out_clean, err_clean = cmd_clean.communicate()
        cmd_update = Popen(["pdsh", "-w", "^" + hosts_file, "-l", "root",
                            "yum", "update", "-y"], stdout=PIPE)
        out_update, err_update = cmd_update.communicate()
        print "Updateing host to %s" % version
        print out_update


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
    try:
        Popen(["aapt"]).communicate()
    except OSError:
        logging.error("Cannot find aapt binary")
        return False

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
    if not out:
        return False
    print "Service %s is running" % (service)
    print "PID: %s" % (list_out[:-1])
    return True


def OpenvpnConnect(username, password, conf_file):
    '''
    Description: Connect to openvpn server
    username = User to connect with
    password = Password to connect with
    conf_file = Configuration file to use
    '''
    log_file = "/tmp/openvpn.log"
    pass_file = "/tmp/.vpn"
    tmp_file = open(pass_file, "w")
    tmp_file.write(username + "\n")
    tmp_file.write(password + "\n")
    tmp_file.close()
    index = 0
    if IsServiceRunnig("openvpn"):
        print "Already connected to VPN server"
        return False

    else:
        openvpn = Popen(["sudo", "openvpn", "--config", conf_file,
                         "--auth-user-pass", pass_file, "--daemon",
                         "--log", log_file], stdout=PIPE)
        out, err = openvpn.communicate()
        clean_tmp_file = Popen(["rm", "-rf", pass_file], stdout=None)
        while index < 30:
            interface = Popen(["ip", "add"], stdout=PIPE)
            intout, interr = interface.communicate()
            redhat0 = re.search("redhat0", intout)
            if not redhat0:
                index += 1
                time.sleep(1)
            else:
                print "Connected to VPN"
                return True
        print "Failed to connect to VPN server"
        return False


def ActionOnRemoteHosts(hosts_file, command, username):
    '''
    Description: Run command on remote linux hosts
    hosts_file = file with hosts to update, one host per line.
    command - command to run on remote hosts.
    username - user for ssh connection to remote host
    '''
    yb = True
    try:
        import yum
        yb = yum.YumBase().isPackageInstalled("pdsh")
    except ImportError:
        logging.info("If this script fails check if pdsh in installed")
        pass

    if not yb:
        print "pdsh is not installed"
        return False

    else:
        cmd = Popen(["pdsh", "-l", username, "-w", "^" + hosts_file, command],
                    stdout=PIPE)
        out, err = cmd.communicate()
        print out


def FindInList(list1=[], list2=[]):
    '''
    Description: Search for items from list1 in list2, return status and new
    list. status 0 mean that the new list is not empty and status 1 mean that
    the new list is empty.
    list1 = list to search from.
    list2 = list to search in.
    '''
    new_list = []
    status = 1
    for val in list1:
        if val in list2:
            new_list.append(val)
            status = 0
        else:
            print "%s not found" % (val)
    return status, new_list


def jenkinsCMD(server, action, view, nview, username=None, password=None,
               search=None):
    '''
    Description: Run action on Jenkins jobs (build, delete, disable, enable,
    get info and print job name)
    server = Jenkins server
    action = action for the job (build, delete, disable, enable, info, print)
    view = view in jenkins (tab)
    nview = nested view in jenkins (under view tab)
    username = username for Jenkins server
    password = password for Jenkins server
    search = search for job name or part of the name
    '''
    try:
        from jenkinsapi.jenkins import Jenkins
    except ImportError:
        logging.error("jenkinsapi is not installed, please install it using: "
                      "pip install jenkinsapi")
        return False

    j = Jenkins(baseurl=server, username=username, password=password)

    view = j.get_view(view)
    nested_view = view.get_nested_view_dict()
    view_url = nested_view.get(nview)
    view_by_url = j.get_view_by_url(view_url)
    jobs_dict = view_by_url.get_job_dict().keys()

    for job in jobs_dict:
        active_job = j.get_job(job)
        if search:
            if search in job:
                if action == "enable":
                    active_job.enable()
                    print job, "enabled"
                if action == "disable":
                    active_job.disable()
                    print job, "disabled"
                if action == "print":
                    print active_job.name
                if action == "build":
                    active_job.post_data(active_job.get_build_triggerurl()[0],
                                         "build")
                    print active_job.name, "building"
                if action == "info":
                    active_job.print_data()
                if action == "delete":
                    j.delete_job(active_job.name)
                    print active_job.name, "Deleted"
                if action == "is_queued":
                    queued = active_job.is_queued()
                    print active_job.name, "queued: ", queued

        else:
            if action == "enable":
                active_job.enable()
                print job, "enabled"
            if action == "disable":
                active_job.disable()
                print job, "disabled"
            if action == "print":
                print active_job.name
            if action == "build":
                active_job.post_data(active_job.get_build_triggerurl()[0],
                                     "build")
                print active_job.name, "building"
            if action == "info":
                    active_job.print_data()
            if action == "delete":
                j.delete_job(active_job.name)
                print active_job.name, "Deleted"
            if action == "is_queued":
                queued = active_job.is_queued()
                print active_job.name, "queued: ", queued

