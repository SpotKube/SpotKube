from optimization_engine.service import service_get_node_configuration
from node_allocator.service_private_cloud import *
from node_allocator.service_aws_cloud import *
from helm_service.service import *

# Private cloud related services

# This function is called when the user wants to start up the private cloud
# First call the optimization engine to get the optimal node configuration
# Then call the node allocator to allocate the nodes to the private cloud
# Then call the helm service to deploy the helm charts
async def startUpPrivateCloud():
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the private cloud
    await service_provision_private_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
# This function is called when the elastic scaler wants to update the private cloud
async def updatePrivateCloud():
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the private cloud
    await service_apply_private_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()

# Public cloud related services

async def startUpAwsCloud():
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the aws cloud
    await service_provision_aws_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
# This function is called when the elastic scaler wants to update the aws cloud
async def updateAwsCloud():
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the aws cloud
    await service_apply_aws_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    