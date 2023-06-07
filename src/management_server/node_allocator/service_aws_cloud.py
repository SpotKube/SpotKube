from .terraform.aws.aws_terraform import *
from .ansible.public_cloud.configure import *

# Destroy aws cloud
async def service_destroy_aws_cloud():
    return await destroy_aws_cloud()

# Destroy and provision aws cloud
async def service_destroy_and_provision_aws_cloud():
    return await destroy_and_provision_aws_cloud()

# Provision aws cloud
async def service_provision_aws_cloud():
    return await provision_aws_cloud()

# Apply changes to aws cloud
async def service_apply_aws_cloud():
    return await apply_aws_cloud()

# Configure aws cloud - Ansible
async def service_configure_aws_cloud():
    return await configure_aws_nodes()

# Write terraform output to a file
async def service_write_terraform_output():
    return await write_terraform_output()
