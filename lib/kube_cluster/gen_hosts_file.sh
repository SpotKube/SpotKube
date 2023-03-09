# Read control_plane_ip and worker_ips from input.json using jq
control_plane_ip=$(jq -r '.control_plane_ip.value[0]' ../env_setup/terraform/terraform_output.json)
worker_ips=$(jq -r '.worker_ips.value | join(" ")' ../env_setup/terraform/terraform_output.json)

# Write the Ansible hosts file
cat > hosts << EOF
[control-plane]
$control_plane_ip ansible_connection=ssh ansible_user=ubuntu

[workers]
EOF

for worker_ip in $worker_ips; do
  echo "$worker_ip ansible_connection=ssh ansible_user=ubuntu" >> hosts
done