import paramiko
import os

hosts_list_org = open("/home/myakove/pdsh-files/all-network-hosts", "r")
hosts_list = [line.strip() for line in hosts_list_org]
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

for host in hosts_list:
    if not os.system("ssh -o ConnectTimeout=5 root@" + host + " exit"):
        print "%s is alive" % host
    else:
        print "%s is down" % host
