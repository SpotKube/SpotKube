# Output VM IP Address
output "private_master_ip" {
  value = openstack_compute_instance_v2.private_master.access_ip_v4
}

output "private_master_floating_ip" {
 value = openstack_networking_floatingip_v2.floating_ip1.address
}

output "private_workers" {
  value = [for instance in openstack_compute_instance_v2.private_workers : {
    private_ip = instance.access_ip_v4
  }]
}

output "private_management_floating_ip" {
  value = data.terraform_remote_state.private_cloud_env_setup.outputs.private_management_floating_ip
}


 