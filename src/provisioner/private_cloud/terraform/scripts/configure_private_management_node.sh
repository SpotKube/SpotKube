#! /bin/bash
set -e

sudo apt update
#Python3
sudo apt install -y python3-pip
sudo pip3 install --upgrade pip
sudo apt install -y python3-venv

# Install ansible
sudo apt install -y software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# Create ansible config file
touch ~/.ansible.cfg
echo "[defaults]" >> ~/.ansible.cfg
echo "host_key_checking = False" >> ~/.ansible.cfg

# Install terraform
sudo apt update
sudo apt install -y gnupg
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update
sudo apt install -y terraform unzip jq

# Check if the key file already exists
if [ ! -f "~/.ssh/id_rsa" ]; then
    # Generate a new SSH key with the given name and no passphrase
    ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa
    echo "New SSH key generated: ~/.ssh/id_rsa"
else
    echo "SSH key already exists: ~/.ssh/id_rsa"
fi

mkdir -p ~/.config/openstack
mv ~/clouds.yaml ~/.config/openstack/

mkdir -p ~/.aws
mv ~/config ~/.aws/
mv ~/credentials ~/.aws/
mv ~/spotkube/ ~/.config/

