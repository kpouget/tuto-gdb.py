#! /usr/bin/bash

HOST_MNT=/home/jcf/host

mkdir -p $HOST_MNT

if [ "$(ls -A $HOST_MNT/dwarf $HOST_MNT/python 2>/dev/null)" ] 
then
    echo ERROR: host directory not empty. Edit and remove this test to continue # :)
    exit
fi

cp dwarf ~/host -r
cp python ~/host -r

cp .gdbinit ~/host/python/gdbinit

echo INFO: Tutorial files copied to ~/host.
