#! /bin/bash

# terraform destroy -auto-approve
terraform init -reconfigure
terraform apply -auto-approve
sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
terraform output -json > private_env_terraform_output.json

# Read the management node floating IP from terraform output
management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' private_env_terraform_output.json)

host_ip=10.8.100.7

# Copy required files to the private host
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/.ssh/id_spotkube spotkube@$host_ip:~/.ssh/
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ./scripts/configure_private_management_node.sh spotkube@$host_ip:~/

# SSH to the private host and then ssh to the management node and run the configure_management_node.sh script
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" -T spotkube@$host_ip <<EOF

mkdir ~/management_node
mv ~/configure_private_management_node.sh ~/management_node/

# copy configure_management_node.sh to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/management_node/configure_private_management_node.sh ubuntu@$management_node_floating_ip:~/

ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" -T ubuntu@$management_node_floating_ip <<DEL1
touch ~/resolv.conf
echo "nameserver 8.8.8.8" > ~/resolv.conf
sudo cp --remove-destination ~/resolv.conf /etc/resolv.conf
DEL1

ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" -T ubuntu@$management_node_floating_ip <<FED1
sudo sed -i '1i127.0.0.1 private-management' /etc/hosts

mkdir ~/scripts
mv ~/configure_private_management_node.sh ~/scripts/
sh ~/scripts/configure_private_management_node.sh

# Generate new SSH key for ansible to use
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa

echo "Configure management node done"
touch ~/management_node_done.txt

FED1
EOF



