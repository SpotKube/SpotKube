from .terraform.private_cloud.private_cloud_terraform import *

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
