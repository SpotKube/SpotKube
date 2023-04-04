# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.private_master_ip.value' ../../terraform/private_cloud/private_instance_terraform_output.json)
worker_ips=$(jq -r '.private_workers.value[].private_ip' ../../terraform/private_cloud/private_instance_terraform_output.json)

# Write the Ansible hosts file
cat > private_hosts << EOF
[control_plane]
$control_plane_ip ansible_connection=ssh ansible_user=ubuntu

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip ansible_connection=ssh ansible_user=ubuntu" >> private_hosts
done