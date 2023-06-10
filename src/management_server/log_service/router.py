from fastapi import APIRouter

from .service import *

log_router = APIRouter(
    prefix="/log",
    tags=["log"],
)

@log_router.get("/")
async def root():
    return {"message": "This is the log service router"}

@log_router.get("/aws_provisioning_log")
async def route_get_aws_provisioning_log():
    return await read_log("aws_cloud_terraform.log")

@log_router.get("/private_provisioning_log")
async def route_get_private_provisioning_log():
    return await read_log("private_cloud_terraform.log")

@log_router.get("/aws_configure_log")
async def route_get_aws_configuring_log():
    return await read_log("aws_cloud_ansible.log")

@log_router.get("/private_configure_log")
async def route_get_private_configuring_log():
    return await read_log("private_cloud_ansible.log")

@log_router.get("/aws_deploy_log")
async def route_get_aws_deploying_log():
    return await read_log("aws_cloud_helm_service.log")

@log_router.get("/private_deploy_log")
async def route_get_private_deploying_log():
    return await read_log("private_cloud_helm_service.log")
