# Output VM IP Address
output "private_management_ip" {
  value = openstack_compute_instance_v2.private_management.access_ip_v4
}

output "private_management_floating_ip" {
 value = openstack_networking_floatingip_v2.floating_ip1.address
}