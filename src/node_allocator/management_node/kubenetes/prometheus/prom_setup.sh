#!/bin/bash

# Install the NFS server on your main system
sudo apt install nfs-kernel-server

# Create a directory to use with Prometheus
sudo mkdir -p /mnt/nfs/promdata

# Change the ownership of the directory
sudo chown nobody:nogroup /mnt/nfs/promdata

# Change the permissions for the directory
sudo chmod 777 /mnt/nfs/promdata
