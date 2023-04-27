# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.control_plane_ip.value[0]' ../../terraform/aws/terraform_output.json)
worker_ips=$(jq -r '.worker_ips.value | join(" ")' ../../terraform/aws/terraform_output.json)

# Write the Ansible hosts file
cat > public_hosts << EOF
[control_plane]
$control_plane_ip ansible_connection=ssh ansible_user=ubuntu

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip ansible_connection=ssh ansible_user=ubuntu" >> public_hosts
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