from .terraform.private_cloud.private_cloud_terraform import *
from .ansible.private_cloud.configure import *

# Destroy private cloud
async def service_destroy_private_cloud():
    await destroy_private_cloud()
    return {"message": "Private cloud destroyed"}

# Destroy and provision private cloud
async def service_destroy_and_provision_private_cloud():
    return await destroy_and_provision_private_cloud()

# Provision private cloud
async def service_provision_private_cloud():
    return await provision_private_cloud()

# Apply changes to private cloud
async def service_apply_private_cloud():
    return await apply_private_cloud()

# Configure private cloud - Ansible
async def service_configure_private_cloud():
    return await configure_private_nodes()

# Write terraform output to a file
async def service_write_terraform_output():
    return await write_terraform_output()
