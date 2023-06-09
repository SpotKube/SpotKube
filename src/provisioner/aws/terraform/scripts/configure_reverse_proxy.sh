#!/bin/bash

management_node="$1"

# Change directory to /etc/nginx
cd /etc/nginx

# Create the 'ssl' directory
sudo mkdir ssl

# Generate SSL certificate
sudo openssl req -batch -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout /etc/nginx/ssl/server.key \
-out /etc/nginx/ssl/server.crt

# Change directory to /etc/nginx/sites-enabled/
cd /etc/nginx/sites-enabled/

# Create or edit the 'fastapi_nginx' file
cat <<EOF | sudo tee fastapi_nginx
server {
    listen 80;
    listen 443 ssl;
    ssl on;
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    server_name $management_node;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
EOF

# Restart the nginx service
sudo service nginx restart