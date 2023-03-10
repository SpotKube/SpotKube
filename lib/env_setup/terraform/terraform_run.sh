#! /bin/bash

terraform destroy -auto-approve -target=aws_instance.management_node -target=aws_instance.worker_node -target=aws_instance.control_plane_node
terraform init
terraform apply -auto-approve
sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
terraform output -json > terraform_output.json

# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.control_plane_ip.value[0]' terraform_output.json)
worker_ips=$(jq -r '.worker_ips.value | join(" ")' terraform_output.json)
management_node_public_ip=$(jq -r '.management_node_public_ip.value' terraform_output.json)

# Write the Ansible hosts file
cat > hosts << EOF
[control_plane]
$control_plane_ip 

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip" >> hosts
done

# Add the Ansible variables to the hosts file
cat >> hosts << EOF

[control_plane:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

[workers:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

EOF

# Copy the Ansible hosts file, terraform output and kube_cluster files to the management node
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr hosts terraform_output.json ../../kube_cluster/ scripts/configure_management_node.sh ubuntu@$management_node_public_ip:~/ansible
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_spotkube -vr ~/.ssh/id_spotkube.pub ~/.ssh/id_spotkube ubuntu@$management_node_public_ip:~/.ssh

# Connect to the remote server
ssh -o StrictHostKeyChecking=no -i "~/.ssh/id_spotkube" ubuntu@$management_node_public_ip <<EOF

cd ansible
sh configure_management_node.sh
cp kube_cluster/.ansible.cfg ~/.ansible.cfg
ansible-playbook -i hosts kube_cluster/initial.yml
ansible-playbook -i hosts kube_cluster/kube-depndencies.yml
ansible-playbook -i hosts kube_cluster/control-plane.yml
EOF