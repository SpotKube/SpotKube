# Environment setup

This folder has all scripts related to environment provisioning.
> Run these scripts in the client computer

## Prerequisites
- Asymmetric key pair named `id_spotkube` and `id_spotkube.pub` *~./ssh* directory. 

## Environment setup will create
- VPC (Virtual Private Cloud)
- Subnet - Public subnet (TODO - a private and a public subnet)
- Internet Gateway
- Route table
- Route table association 
- Security group - Allow SSH (TODO - Allow HTTP, HTTPS)
- Management node (EC2 instance: t2-micro) - Install Ansible and Terraform. Create new key pair `id_rsa`. Copy AWS keys.

## Terraform outputs
- Subnet
- Security group SSH
