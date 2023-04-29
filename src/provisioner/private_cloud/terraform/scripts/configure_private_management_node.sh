#! /bin/bash
set -e

# Install terraform
sudo apt-add-repository --yes --update ppa:ansible/ansible
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list

# Install helm
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt install apt-transport-https --yes
sudo apt install helm --yes

#Python3
sudo apt install -y python3-pip python3-venv

# Install ansible
sudo apt install -y software-properties-common ansible

# Create ansible config file
touch ~/.ansible.cfg
echo "[defaults]" >> ~/.ansible.cfg
echo "host_key_checking = False" >> ~/.ansible.cfg

# Install terraform
sudo apt install -y gnupg terraform unzip jq

mkdir -p ~/.config/openstack
mv ~/clouds.yaml ~/.config/openstack/

mkdir -p ~/.aws
mv ~/config ~/.aws/
mv ~/credentials ~/.aws/
rm -r ~/.config/spotkube
mv ~/spotkube/ ~/.config/

# Check if the key file already exists
if [ ! -f ~/.ssh/id_rsa ]; then
# Generate a new SSH key with the given name and no passphrase
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa
echo "New SSH key generated: ~/.ssh/id_rsa"
else
echo "SSH key already exists: ~/.ssh/id_rsa"
fi

