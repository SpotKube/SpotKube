# Output VM IP Address
output "private_management_ip" {
  value = openstack_compute_instance_v2.private_management.access_ip_v4
}

output "private_management_floating_ip" {
 value = openstack_networking_floatingip_v2.floating_ip1.address
}

# Private network name
output "private_network_name" {
  value = openstack_networking_network_v2.private_network.name
}

# Private subnet name
output "private_subnet_name" {
  value = openstack_networking_subnet_v2.private_subnet.name
}

# Private security group name - ssh access
output "private_ssh_security_group_name" {
  value = openstack_compute_secgroup_v2.ssh_access_group.name
}

