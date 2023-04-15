#! /bin/bash

# terraform destroy -auto-approve -var-file="private.tfvars"
# terraform init
# terraform apply -auto-approve -var-file="private.tfvars"
# sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
terraform output -json > private_instance_terraform_output.json

# # Read the management node floating IP from terraform output
management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' private_instance_terraform_output.json)

host_ip=10.8.100.7

# Copy required files to the private host
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ../../../../node_allocator spotkube@$host_ip:~/

# SSH to the private host and then ssh to the management node and run the configure_management_node.sh script
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" -T spotkube@$host_ip <<EOF

# # copy node_allocator to the management node
scp -o StrictHostKeyChecking=no -i $PRIVATE_INSTANCE_SSH_KEY_PATH -vr ~/node_allocator ubuntu@$management_node_floating_ip:~/
scp -o StrictHostKeyChecking=no -i $PRIVATE_INSTANCE_SSH_KEY_PATH -vr $PRIVATE_INSTANCE_SSH_KEY_PATH ubuntu@$management_node_floating_ip:~/.ssh/

ssh -o StrictHostKeyChecking=no -i "$PRIVATE_INSTANCE_SSH_KEY_PATH" -T ubuntu@$management_node_floating_ip <<FED1

cd ~/node_allocator/management_node/ansible/scripts
rm hosts private_hosts
sh gen_private_hosts_file.sh
cp private_hosts ../hosts
cd ../
cp .ansible.cfg ~/.ansible.cfg
ansible-playbook -i hosts initial.yml
ansible-playbook -i hosts kube-depndencies.yml
ansible-playbook -i hosts control-plane.yml

echo "Configure management node done"
touch ~/management_node_done.txt

FED1
EOF



