#! /bin/bash

terraform destroy -auto-approve
terraform init
terraform apply -auto-approve
sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
terraform output -json > terraform_output.json

# Read the management node floating IP from terraform output
management_node_floating_ip=$(jq -r '.private_management_floating_ip.value' terraform_output.json)

host_ip=10.8.100.7
# SSH to the private host
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" spotkube@$host_ip <<EOF

  sh ./scripts/configure_private_management_node.sh

EOF


# # Copy the Ansible hosts file, terraform output and kube_cluster files to the management node
# scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr hosts terraform_output.json ../../kube_cluster/ scripts/configure_management_node.sh ubuntu@$management_node_public_ip:~/ansible
# scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/.ssh/id_spotkube.pub ~/.ssh/id_spotkube ubuntu@$management_node_public_ip:~/.ssh

# # Connect to the remote server
# ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF

# cd ansible
# sh configure_management_node.sh
# cp kube_cluster/.ansible.cfg ~/.ansible.cfg
# ansible-playbook -i hosts kube_cluster/initial.yml
# ansible-playbook -i hosts kube_cluster/kube-depndencies.yml
# ansible-playbook -i hosts kube_cluster/control-plane.yml
# EOF