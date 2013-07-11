#! /usr/bin/python

import re
import os
import user
import time
import smtplib
import logging
from subprocess import Popen, PIPE
from commands import getoutput

LIST = []
COLORS = {"black": "\033[0;30m",
          "dark_gray": "\033[1;30m",
          "blue": "\033[0;34m",
          "light_blue": "\033[1;34m",
          "green": "\033[0;32m",
          "light_green": "\033[1;32m",
          "cyan": "\033[0;36m",
          "light_cyan": "\033[1;36m",
          "red": "\033[0;31m",
          "light_red": "\033[1;31m",
          "purple": "\033[0;35m",
          "light_purple": "\033[1;35m",
          "brown": "\033[0;33m",
          "yellow": "\033[1;33m",
          "light_gray": "\033[0;37m",
          "white": "\033[1;37m",
          "clear": "\033[0m"}


def autoSSH(host, username, password, connect=False):
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

    if not yb:
        print "sshpass is not installed"
        return False

    else:
        home = user.home
        ssh_dir = ".ssh"
        ssh_file = "known_hosts"
        ssh_path = home + '/' + ssh_dir + '/' + ssh_file
        know_host = open(ssh_path, "r").readlines()

        host_ip = Popen(["host", host], stdout=PIPE,
                        shell=False).communicate()[0]
        host_ip_addr = host_ip.split()

        for line in know_host:
            if host in line:
                Popen(["ssh-keygen", "-R", host], stdout=PIPE, shell=False)
            if host_ip_addr[3] in line:
                Popen(["ssh-keygen", "-R", host_ip_addr[3]], stdout=PIPE,
                      shell=False)

        host_key = Popen(["ssh-keyscan", "-T", "5", host],
                         stdout=PIPE, shell=False).communicate()[0]

        if host_key == "":
            err_output = "".join([COLORS["red"], " No ssh keys from %s",
                                  COLORS["clear"]])
            print err_output % host
            return False

        else:
            echo_cmd = 'echo " ' + host_key + '" >> ' + ssh_path
            Popen([echo_cmd], stdout=PIPE, shell=True)

        Popen(["sshpass", "-p", password, "ssh-copy-id",
               username + "@" + host], stdout=PIPE).communicate()

        if connect:
            cmd_line = "".join(["ssh ", username + "@" + host])
            Popen([cmd_line], shell=True).communicate()

    return True


def hostAlive(host):
    '''
    Description: Check if remote host is alive using ssh
    host = host to connect to
    '''
    if not os.system("ssh -o ConnectTimeout=5 root@" + host +
                     " exit &> /dev/null"):
        return False
    return True


def updateRepoAndInstall(version, host, yum_clean=False):
    '''
    Description: Update rhevm.repo to desire build and update the hosts
    version = build version to update to.
    hosts_file = file with hosts to update, one host per line.
    '''
    linux_user = "root"
    repo_dir = "/etc/yum.repos.d/"
    tmp_file = "/tmp/rhevm.repo"

    repo_file = open(tmp_file, "w")
    repo_file.write("[rhevm]" + "\n")
    repo_file.write("name=RHEVM" + "\n")
    repo_file.write("baseurl=http://bob.eng.lab.tlv.redhat.com/builds/" +
                    version + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.write("enable=1" + "\n")
    repo_file.write("\n\n")

    repo_file.write("[rhel]" + "\n")
    repo_file.write("name=RHEL_64" + "\n")
    repo_file.write("baseurl=http://download.eng.tlv.redhat.com/pub/rhel/" +
                    "released/RHEL-6/6.4/Server/x86_64/os/" + "\n")
    repo_file.write("enabled=1" + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.write("\n\n")

    repo_file.write("[rhel-zstream]" + "\n")
    repo_file.write("name=RHEL_64_Z" + "\n")
    repo_file.write("baseurl=http://download.eng.tlv.redhat.com/rel-eng/" +
                    "repos/RHEL-6.4-Z/x86_64/" + "\n")
    repo_file.write("enabled=1" + "\n")
    repo_file.write("gpgcheck=0" + "\n")
    repo_file.close()

    cmd_yum = Popen(["ssh", linux_user + "@" + host, "ps -ef | grep yum | \
                     grep -v grep"],
                    stdout=PIPE, stderr=PIPE, shell=False)
    out_yum = cmd_yum.communicate()[0]
    if out_yum:
        print "yum already in progress, host: ",\
            COLORS["brown"], host, COLORS["clear"]
        return False

    cmd_scp = Popen(["scp", tmp_file, linux_user + "@" + host + ":" +
                     repo_dir],
                    stdout=PIPE, stderr=PIPE, shell=False)
    err_scp = cmd_scp.communicate()[1]

    if err_scp:
        print err_scp
        print "Fail to copy repo file to :",\
            COLORS["brown"], host, COLORS["clear"]
        return False

    if yum_clean:
        actionOnRemoteHosts(host, "yum clean all", linux_user)

    yum_update = actionOnRemoteHosts(host, "yum update -y", linux_user)

    if not yum_update:
        err = "".join(["Failed to update ", COLORS["brown"], host,
                       COLORS["clear"], " to version ", COLORS["brown"],
                       version, COLORS["clear"]])
        print err
        return False
    return True


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
    macout = mac.communicate()[0]
    ip = Popen((["ssh -o ConnectTimeout=5 root@" + host + " ifconfig " +
                 interface + " | grep 'inet addr' |cut -d':' -f2|awk \
                 '{print $1}'"]), shell=True, stdout=PIPE)
    ipout = ip.communicate()[0]
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
    fdout = cmd.communicate()[1]

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


def ldapSearchOLD(name):
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
            err_output = "".join([COLORS["red"], "User not found",
                                  COLORS["clear"]])
            print COLORS["brown"], name, COLORS["clear"], err_output
            return False

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
                    new_line = line.split(" ")
                    param = new_line[1:]
                    title = new_line[0].replace(key, param_dict[key])
                    output = "".join([COLORS["light_green"], title,
                                      COLORS["clear"], " ".join(param)])
                    print output
    print '\n'
    return True


def isServiceRunnig(service):
    '''
    Description: Check if service is running, retur PID of the service.
    service = service to search for.
    '''
    cmd = Popen(["pgrep", service], stdout=PIPE)
    out = cmd.communicate()[0]
    list_out = out.split("\n")
    if not out:
        return False
    print "Service %s is running" % (service)
    print "PID: %s" % (list_out[:-1])
    return True


def openvpnConnect(username, password, conf_file):
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
    if isServiceRunnig("openvpn"):
        print "Already connected to VPN server"
        return False

    else:
        Popen(["sudo", "openvpn", "--config", conf_file,
               "--auth-user-pass", pass_file, "--daemon",
               "--log", log_file], stdout=PIPE).communicate()
        Popen(["rm", "-rf", pass_file], stdout=None)
        while index < 30:
            interface = Popen(["ip", "add"], stdout=PIPE)
            intout = interface.communicate()[0]
            redhat0 = re.search("redhat0", intout)
            if not redhat0:
                index += 1
                time.sleep(1)
            else:
                print "Connected to VPN"
                return True
        print "Failed to connect to VPN server"
        return False
    return True


def actionOnRemoteHosts(host, command, username):
    '''
    Description: Run command on remote linux hosts
    host = host to run the remote command.
    command - command to run on remote hosts.
    username - user for ssh connection to remote host
    '''
    remote_command = "".join("ssh " + username + "@" + host + " " + command)
    cmd = Popen([remote_command], stdout=PIPE, stderr=PIPE, shell=True)
    out, err = cmd.communicate()
    if err:
        print err
        return False
    output = "".join([COLORS["brown"], host + ": " + COLORS["clear"], out])
    print output
    return out


def findInList(list1=list(), list2=list()):
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
    action = action for the job (build, delete, disable, enable, info, print,
             is_queue, is_running)
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
                    print COLORS["brown"], job, COLORS["clear"], "enabled"
                if action == "disable":
                    active_job.disable()
                    print COLORS["brown"], job, COLORS["clear"], "disabled"
                if action == "print":
                    print COLORS["brown"], active_job.name
                if action == "build":
                    active_job.post_data(active_job.get_build_triggerurl()[0],
                                         "build")
                    print COLORS["brown"], active_job.name, COLORS["clear"], \
                        "building"
                if action == "info":
                    active_job.print_data()
                if action == "delete":
                    j.delete_job(active_job.name)
                    print COLORS["brown"], active_job.name, COLORS["clear"], \
                        "Deleted"
                if action == "is_queued":
                    queued = active_job.is_queued()
                    print COLORS["brown"], active_job.name, COLORS["clear"], \
                        "queued: ", queued
                if action == "is_running":
                    running = active_job.is_running()
                    print COLORS["brown"], active_job.name, COLORS["clear"], \
                        "running: ", running

        else:
            if action == "enable":
                active_job.enable()
                print COLORS["brown"], job, COLORS["clear"], "enabled"
            if action == "disable":
                active_job.disable()
                print COLORS["brown"], job, COLORS["clear"], "disabled"
            if action == "print":
                print COLORS["brown"], active_job.name
            if action == "build":
                active_job.post_data(active_job.get_build_triggerurl()[0],
                                     "build")
                print COLORS["brown"], active_job.name, COLORS["clear"], \
                    "building"
            if action == "info":
                active_job.print_data()
            if action == "delete":
                j.delete_job(active_job.name)
                print COLORS["brown"], active_job.name, COLORS["clear"], \
                    "Deleted"
            if action == "is_queued":
                queued = active_job.is_queued()
                print COLORS["brown"], active_job.name, COLORS["clear"], \
                    "queued: ", queued
            if action == "is_running":
                    running = active_job.is_running()
                    print COLORS["brown"], active_job.name, COLORS["clear"], \
                        "running: ", running


def sendEmail(server, msg, mail_from, mail_to, server_port=None):
    '''
    Basic function to send email
    server = SMTP server
    msg = the email to send
    mail_from = mail from address
    mail_to = mail to address
    server_port = SMTP server port if needed
    '''
    if server_port:
        server = smtplib.SMTP(server, server_port)
        if not server:
            print "Failed to connect to SMTP server %s" % server
            return False

    server = smtplib.SMTP(server)
    if not server:
        print "Failed to connect to SMTP server %s" % server
        return False

    server.sendmail(mail_from, mail_to, msg)
    print "Sending email to %s" % mail_to
    return True


def ldapSearch(server, user, domain, port=389):
    try:
        import ldap
    except ImportError:
        logging.error("python-ldap is not installed")
        return False

    searchScope = ldap.SCOPE_SUBTREE
    ldap_server = ldap.open(host=server, port=port)
    basedomain = domain.split(".")
    baseDN = "".join(["dc=", basedomain[0], ",dc=", basedomain[1]])
    retrieveAttributes = ["dn", "cn", "uid", "mail", "telephoneNumber",
                          "mobile", "rhatLocation", "rhatCostCenterDesc"]

    param_dict = {'dn:': 'dn', 'cn:': 'Full Name:      ', 'uid:': 'IRC:     ' +
                  '       ', 'mail:': 'Email:          ', 'telephoneNumber:':
                  'Office Ext:     ', 'mobile:': 'Mobile Phone:   ',
                  'rhatLocation:': 'Office Location:', 'rhatCostCenterDesc:':
                  'Job Title:      '}

    match = False
    for val in retrieveAttributes:
        ldap_result_id = ldap_server.search(base=baseDN,
                                            scope=searchScope,
                                            filterstr="".join([val, "=*",
                                                               user, "*"]),
                                            attrlist=retrieveAttributes)
        result_type, result_data = ldap_server.result(ldap_result_id, 0)
        if len(result_data) > 0:
            out, data = result_data[0]
            for key in data.keys():
                new_key = key.replace(key, param_dict[key+":"])
                value = data[key][0]
                print COLORS["light_green"], new_key, COLORS["clear"], value
                match = True
            print "**********************************************"

    if not match:
        err = "".join(["User ", COLORS["red"], user,  COLORS["clear"],
                       " not found"])
        print err
        return False
    return True

