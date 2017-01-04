#!/bin/bash

cat <<EOF
##########
#
# Understanding, Scripting and Extending GDB
#
##########
#
##########
# Running an Archlinux container
##########
EOF

##### check env #####

if [ -z "$USERID" ]
then
  echo "FATAL: USERID/GROUPID environment variables not set. Did you pass it to docker?" 
  echo "       Please run docker as follows:"
  cat <<EOF

HOST_DIR=\$HOME/gdb_data # create it first !
docker run -it -v \$HOST_DIR:/home/gdb/host -e GROUPID=\$(id -g) -e USERID=\$(id -u) --cap-add sys_ptrace kpouget/tuto-gdb.py
EOF
   exec bash
fi

##### admin stuff #####

echo "root:root" | chpasswd && echo "INFO: root password set to 'root'."
groupadd --gid $GROUPID gdb --non-unique
useradd --uid $USERID --gid $GROUPID gdb
chown gdb:gdb /home/gdb/ -R
echo "INFO: Docker image version $(cat /home/gdb/.version)"
##### check strace #####

strace ls &>/dev/null
if [ $? -eq 1 ] 
then
    echo 'ERROR: ptrace not working. Did you pass --privileged or --cap-add sys_ptrace option to docker ?'
fi

##### prepare host #####

HOST_MNT=/home/gdb/host
if [ -z "$(ls -A $HOST_MNT/dwarf $HOST_MNT/python 2>/dev/null)" ] 
then
    echo "INFO: Running './prepare_host.sh' to populate $HOST_MNT host-shared directory."
    su gdb -c ./prepare_host.sh
fi

echo "INFO: Read ~/README or ~/presentation.pdf for usage details"

exec su gdb
