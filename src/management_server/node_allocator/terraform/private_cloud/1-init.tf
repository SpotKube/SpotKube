# Configure the OpenStack Provider
provider "openstack" {
  cloud  = "openstack" # cloud defined in cloud.yml file
}

data "terraform_remote_state" "private_cloud_env_setup" {
  backend = "s3"

  config = {
    bucket = "spotkube-terraform-state-bucket"
    key    = "private_cloud_env_setup-terraform.tfstate"
    region = "us-west-2"
  }
}


# Data sources
## Get Image ID
data "openstack_images_image_v2" "image" {
  name        = "Ubuntu-22" # Name of image to be used
  most_recent = true

  properties = {
    key = "value"
  }
}

## Get flavor id
data "openstack_compute_flavor_v2" "flavor" {
  name = "m1.medium" # flavor to be used
}

# Get public network
data "openstack_networking_network_v2" "public_network" {
  name = "public"
}

# Get private subnet
data "openstack_networking_subnet_v2" "private_subnet" {
  name = data.terraform_remote_state.private_cloud_env_setup.outputs.private_subnet_name
}

# Create the master node
resource "openstack_compute_instance_v2" "private_master" {
  name            = "Private_Master"  #Instance name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair
  security_groups = [data.terraform_remote_state.private_cloud_env_setup.outputs.private_ssh_security_group_name, "default"]
  depends_on = [data.openstack_networking_subnet_v2.private_subnet]

  network {
    name = data.terraform_remote_state.private_cloud_env_setup.outputs.private_network_name
  }
}

resource "openstack_networking_floatingip_v2" "floating_ip1" {
  pool = "public"
}

resource "openstack_compute_floatingip_associate_v2" "private_master_floating_ip" {
  floating_ip = openstack_networking_floatingip_v2.floating_ip1.address
  instance_id = openstack_compute_instance_v2.private_master.id
}