# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.private_master_ip.value' ../../terraform/private_cloud/private_instance_terraform_output.json)
worker_ips=$(jq -r '.private_workers.value[].private_ip' ../../terraform/private_cloud/private_instance_terraform_output.json)

# Write the Ansible hosts file
cat > private_hosts << EOF
[control_plane]
$control_plane_ip

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip" >> private_hosts
done

# Add the Ansible variables to the hosts file
cat >> private_hosts << EOF

[control_plane:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

[workers:vars]
ansible_connection=ssh
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_spotkube

EOF