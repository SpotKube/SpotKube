# Private Cloud Setup
This repository contains instructions to set up a private cloud environment using OpenStack client and Terraform.

## Installation
To install and configure the OpenStack client on Linux, please follow the instructions provided in [this guide](https://computingforgeeks.com/install-and-configure-openstack-client-on-linux/).

## Deployment
To deploy a virtual machine instance on OpenStack using Terraform, follow the instructions provided in [this guide](https://computingforgeeks.com/deploy-vm-instance-on-openstack-with-terraform/).


### Upload image to glance
Go to the directory where image is located and update variables to match your OpenStack environment. When done, source 
the file to start using openstack command line tool to administer OpenStack Cloud.

```
openstack image create \
    --container-format bare \
    --disk-format qcow2 \
    --file ubuntu-22.04-server-cloudimg-amd64.img \
    Ubuntu-22
```

### Upload the public key to Openstack. This key will be used during instance creation for passwordless authentication

Generate new SSH key if you don’t have one already.
`ssh-keygen`

```
openstack keypair create --public-key ~/.ssh/id_spotkube.pub admin
```

### Add cloud.yaml file

`mkdir ~/.config/openstack/`

Download the `cloud.yaml` file from horizon and copy into the above created directory.
