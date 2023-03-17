# Configure the OpenStack Provider
provider "openstack" {
  cloud  = "openstack" # cloud defined in cloud.yml file
}

# Data sources
## Get Image ID
data "openstack_images_image_v2" "image" {
  name        = "Debian-10" # Name of image to be used
  most_recent = true

  properties = {
    key = "value"
  }
}

## Get flavor id
data "openstack_compute_flavor_v2" "flavor" {
  name = "m1.small" # flavor to be used
}

resource "openstack_networking_network_v2" "private_network" {
  name = "private_network"
}

resource "openstack_networking_subnet_v2" "private_subnet" {
  name         = "private_subnet"
  cidr         = "10.0.1.0/24"
  network_id   = openstack_networking_network_v2.private_network.id
  enable_dhcp  = true
  ip_version   = 4
}

# Create an instance
resource "openstack_compute_instance_v2" "server" {
  name            = "Debian"  #Instance name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair
  security_groups = var.security_groups

  network {
    name = "${openstack_networking_network_v2.private_network.name}"
  }
}

# Output VM IP Address
output "serverip" {
  value = openstack_compute_instance_v2.server.access_ip_v4
}