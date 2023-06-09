#!/bin/bash

# Exit if three arguments are not passed
if [ $# -ne 3 ]; then
    echo "Usage: $0 <management_server_ip> <prometheus_ip> <grafana_ip>"
    exit 1
fi

# Install nginx
sudo apt update
sudo apt install nginx -y

# Enable nginx
sudo systemctl enable nginx.service

# Export variables
export MGT_SERVER=$1
export PROMETHEUS=$2
export GRAFANA=$3

# Create nginx config
envsubst < nginx.conf > spotkube.conf
sudo cat spotkube.conf > /etc/nginx/sites-available/spotkube
# Create symlink
sudo ln -s /etc/nginx/sites-available/spotkube /etc/nginx/sites-enabled/

sudo systemctl restart nginx.service
