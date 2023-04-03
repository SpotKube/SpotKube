#!/bin/bash

# Specify the name server you want to use
nameserver="8.8.8.8"

touch ~/resolv.conf
echo "nameserver $nameserver" > ~/resolv.conf
sudo cp ~/resolv.conf /etc/resolv.conf
