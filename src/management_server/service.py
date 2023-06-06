from optimization_engine.service import service_get_node_configuration
from node_allocator.service_private_cloud import *
from node_allocator.service_aws_cloud import *
from helm_service.service import *
import time
from utils import get_logger

current_dir = os.getcwd()
logger_dir = os.path.join(current_dir, "logs")

logger = get_logger(path=logger_dir, log_file="management_server.log")

# Private cloud related services

# This function is called when the user wants to start up the private cloud
# First call the optimization engine to get the optimal node configuration
# Then call the node allocator to allocate the nodes to the private cloud
# Then call the helm service to deploy the helm charts
async def startUpPrivateCloud():
    # Start measuring the time
    start_time = time.time()
    
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the private cloud
    await service_provision_private_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("Total time taken to start up the private cloud: " + str(elapsed_time) + " seconds")
    
# This function is called when the elastic scaler wants to update the private cloud
async def updatePrivateCloud():
    # Start measuring the time
    start_time = time.time()
    
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the private cloud
    await service_apply_private_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("Total time taken to update the private cloud: " + str(elapsed_time) + " seconds")

# Public cloud related services

async def startUpAwsCloud():
    # Start measuring the time
    start_time = time.time()
    
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the aws cloud
    await service_provision_aws_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("Total time taken to start up the aws cloud: " + str(elapsed_time) + " seconds")
    
    
    
# This function is called when the elastic scaler wants to update the aws cloud
async def updateAwsCloud():
    # Start measuring the time
    start_time = time.time()
    
    # Get optimal node configuration
    await service_get_node_configuration("greedy_v2")
    
    # Allocate the nodes to the aws cloud
    await service_apply_aws_cloud()
    
    # Deploy the helm charts
    await deploy_helm_charts()
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info("Total time taken to update the aws cloud: " + str(elapsed_time) + " seconds")
    