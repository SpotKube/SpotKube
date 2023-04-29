# Create instances
resource "openstack_compute_instance_v2" "private_workers" {
  for_each             = var.private_instances
  name            = each.key  #Instance name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair
  security_groups = [data.terraform_remote_state.private_cloud_env_setup.outputs.private_ssh_security_group_name, "default"]
  depends_on = [data.openstack_networking_subnet_v2.private_subnet]

  network {
    name = data.terraform_remote_state.private_cloud_env_setup.outputs.private_network_name
  }
}