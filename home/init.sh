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

HOST_DIR=$HOME/gdb.py_data # create it first !
docker run -it -v \$HOST_DIR:/home/gdb.py/host -e GROUPID=\$(uid -g) -e USERID=\$(uid -u) --cap-add sys_ptrace kpouget/tuto-gdb.py
EOF
   exec bash
fi

##### admin stuff #####

echo "root:root" | chpasswd && echo "INFO: root password set to 'root'."
groupadd --gid $GROUPID jcf --non-unique
useradd --uid $USERID --gid $GROUPID jcf
chown jcf:jcf /home/jcf/ -R
echo "INFO: Docker image version $(cat /home/jcf/.version)"
##### check strace #####

strace ls &>/dev/null
if [ $? -eq 1 ] 
then
    echo 'ERROR: ptrace not working. Did you pass --privileged or --cap-add sys_ptrace option to docker ?'
fi

##### prepare host #####

HOST_MNT=/home/jcf/host
if [ -z "$(ls -A $HOST_MNT/dwarf $HOST_MNT/python 2>/dev/null)" ] 
then
    echo "INFO: Running './prepare_host.sh' to populate $HOST_MNT host-shared directory."
    su jcf -c ./prepare_host.sh
fi

echo "INFO: Read ~/README or ~/presentation.pdf for usage details"

exec su jcf
