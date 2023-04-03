# Output VM IP Address
output "private_master_ip" {
  value = openstack_compute_instance_v2.private_master.access_ip_v4
}

output "private_master_floating_ip" {
 value = openstack_networking_floatingip_v2.floating_ip1.address
}