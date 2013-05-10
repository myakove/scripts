yum install -y `curl -k $1 | grep x86_64 | awk -F'"' {'print $4'}`
