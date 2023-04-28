#! /bin/bash

source "../../../../../.config/provisioner.conf"

terraform destroy -auto-approve -var-file="private.tfvars"
terraform init
terraform apply -auto-approve -var-file="private.tfvars"
sleep 60 # Wait for 60 seconds to ensure the instances are fully provisioned
terraform output -json > private_instance_terraform_output.json


cd ~/management_server/node_allocator/ansible/scripts
rm hosts private_hosts
sh gen_private_hosts_file.sh
cp private_hosts ../hosts
cd ../
cp .ansible.cfg ~/.ansible.cfg

ansible-playbook -i hosts initial.yml
ansible-playbook -i hosts kube-depndencies.yml
ansible-playbook -i hosts control-plane.yml




