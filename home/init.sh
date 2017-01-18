#!/bin/bash

cat <<EOF
##########
#
# Understanding, Scripting and Extending GDB, interactive part
#
##########
EOF
##########


##### ENVIRONMENT #####

HOST_MNT=/home/gdb/host
USER_NAME=gdb
IMAGE_NAME=kpouget/tuto-gdb.py

##### admin stuff #####


echo "##########"
echo "# Running an Archlinux container"
echo "# Docker image built on $(cat /home/$USER_NAME/.version)"
echo "##########"
echo

GROUPID=$(stat $HOST_MNT -c %g)
USERID=$(stat $HOST_MNT -c %u)

if [[ $USERID -eq 0 && $GROUPID -eq 0 ]]
then

    echo "####################"
    echo "WARNING: Directory '$HOST_MNT' not shared with host, is it on purpose ? if not, please use this command line:"
    echo "    HOST_DIR=\$HOME/${USER_NAME}_data; mkdir -p \$HOST_DIR"
    echo "    docker run --rm -it -v \$HOST_DIR:/home/$USER_NAME/host  --cap-add sys_ptrace $IMAGE_NAME"
    echo "####################"
    echo
    GROUPID=1000
    USERID=1000
    NO_HOST=1
fi

echo "root:root" | chpasswd 

groupadd --gid $GROUPID $USER_NAME --non-unique
useradd --uid $USERID --gid $GROUPID $USER_NAME

chown $USER_NAME:$USER_NAME /home/$USER_NAME/ -R

##### check strace #####

strace ls &>/dev/null
if [ $? -eq 1 ] 
then
    echo "####################"
    echo 'ERROR: ptrace not working. Did you pass --privileged or --cap-add sys_ptrace option to docker ?'
    echo "####################"
    echo
fi

##### prepare host #####

if [[ -z "$NO_HOST" && -z "$(ls -A $HOST_MNT/dwarf $HOST_MNT/python 2>/dev/null)" ]]
then
    echo "INFO: Running './prepare_host.sh' to populate $HOST_MNT host-shared directory."
    su  $USER_NAME -c ./prepare_host.sh
fi

echo "INFO: Read ~/README, ~/presentation.pdf and ~/exercices.md for usage details"
echo

exec su $USER_NAME
