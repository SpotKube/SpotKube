#! /bin/bash
set -e

source "../../../common/scripts/common_pkg_installer.sh"

# Create anisble config file
sudo apt-get update
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
