# Configure the OpenStack Provider
provider "openstack" {
  cloud  = "openstack" # cloud defined in cloud.yml file
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
  name = "m1.small" # flavor to be used
}

#Create a private network
resource "openstack_networking_network_v2" "private_network" {
  name = "private_network"
}

# Create a subnet for the private network
resource "openstack_networking_subnet_v2" "private_subnet" {
  name         = "private_subnet"
  cidr         = "10.0.1.0/24"
  network_id   = openstack_networking_network_v2.private_network.id
  enable_dhcp  = true
  ip_version   = 4
}

# Create public network
data "openstack_networking_network_v2" "public_network" {
  name = "public"
}

# Create a router and connect it to the public network
resource "openstack_networking_router_v2" "router" {
  name = "router"

  external_network_id = data.openstack_networking_network_v2.public_network.id
}

# Connect the router to the private network
resource "openstack_networking_router_interface_v2" "router_interface" {
  router_id   = openstack_networking_router_v2.router.id
  subnet_id   = openstack_networking_subnet_v2.private_subnet.id
}

# Create security access group
resource "openstack_compute_secgroup_v2" "ssh_access_group" {
  name        = "ssh_access_group"
  description = "a security group"

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

# Create an instance
resource "openstack_compute_instance_v2" "private_master" {
  name            = "Private_Master"  #Instance name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair
  security_groups = [openstack_compute_secgroup_v2.ssh_access_group.name, "default"]

  network {
    name = "${openstack_networking_network_v2.private_network.name}"
  }
}

# Create an instance
resource "openstack_compute_instance_v2" "private_worker" {
  name            = "Private_Worker"  #Instance name
  image_id        = data.openstack_images_image_v2.image.id
  flavor_id       = data.openstack_compute_flavor_v2.flavor.id
  key_pair        = var.keypair
  security_groups = [openstack_compute_secgroup_v2.ssh_access_group.name, "default"]

  network {
    # name = "${openstack_networking_network_v2.private_network.name}"
    port = "${openstack_networking_port_v2.port_1.id}"
  }
}

resource "openstack_networking_floatingip_v2" "private_master_floating_ip" {
  pool = "public"
}

resource "openstack_compute_floatingip_associate_v2" "private_master_floating_ip" {
  floating_ip = openstack_networking_floatingip_v2.private_master_floating_ip.address
  instance_id = openstack_compute_instance_v2.private_master.id
}

resource "openstack_networking_floatingip_v2" "private_worker_floating_ip" {
  pool = "public"
}

resource "openstack_compute_floatingip_associate_v2" "private_worker_floating_ip" {
  floating_ip = openstack_networking_floatingip_v2.private_worker_floating_ip.address
  instance_id = openstack_compute_instance_v2.private_worker.id
}