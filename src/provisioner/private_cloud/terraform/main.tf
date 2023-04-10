
# Configure the OpenStack Provider
terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
    }
  }

  backend "s3" {
    bucket = "spotkube-terraform-state-bucket"
    key    = "private_cloud_env_setup-terraform.tfstate"
    region = "us-west-2"
  }
}