#! /bin/bash
set -e

source "../../../../scripts/common.sh"
source "../../../common/scripts/common_pkg_installer.sh"

# Create anisble config file
sudo apt-get update

rm -f ~/.ansible.cfg
touch ~/.ansible.cfg
echo "[defaults]" >> ~/.ansible.cfg
echo "host_key_checking = False" >> ~/.ansible.cfg

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
rm -rf aws
unzip awscliv2.zip
sudo ./aws/install --update

# Generate key pair
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1

# Create directory if not exists
mkdir -p ~/.aws

# Install helm
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
sudo apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
sudo apt-get update
sudo apt-get install helm --yes

# Cleanup
rm -rf awscliv2.zip aws kubectl

print_info "Instalation completed successfully"
