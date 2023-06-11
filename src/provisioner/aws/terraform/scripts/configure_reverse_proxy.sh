#!/bin/bash

management_node="$1"

# Change directory to /etc/nginx
cd /etc/nginx/sites-available

# Create or edit the 'mgt_server' file
cat <<EOF | sudo tee spotkube
# Management server API
server {
    listen 80;
    server_name ${MGT_SERVER};
    location / {
        proxy_pass http://localhost:8000;
    }
}
EOF

# Create symlink
sudo ln -s /etc/nginx/sites-available/spotkube /etc/nginx/sites-enabled/

# Restart the nginx service
sudo systemctl restart nginx.service