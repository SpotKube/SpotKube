#!/bin/bash

sudo apt update
#Python3
sudo apt install -y python3-pip
sudo pip3 install --upgrade pip
sudo apt install -y python3-venv
sudo apt install -y nginx
sudo apt install -y openssl

# Install ansible
sudo apt install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

sudo apt install -y gnupg

# Install terraform
sudo apt update
sudo apt install -y gnupg
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install -y terraform unzip jq

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -rf kubeclt

# Install nginx
sudo apt update
sudo apt install -y nginx
# Enable nginx service
sudo systemctl enable nginx.service
sudo systemctl start nginx.service

# Install golang
curl -OL https://go.dev/dl/go1.20.5.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.20.5.linux-amd64.tar.gz
rm -rf go1.20.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
source ~/.bashrc

# Install k9s
curl -sS https://webinstall.dev/k9s | bash
source ~/.config/envman/PATH.env
