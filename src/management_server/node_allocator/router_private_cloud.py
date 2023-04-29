from fastapi import APIRouter

from .service_private_cloud import *

# Private cloud
na_private_router = APIRouter(
    prefix="/node_allocator/private",
    tags=["node_allocator"],
)

@na_private_router.get("/")
async def root():
    return {"message": "This is the node allocator private cloud router"}

@na_private_router.get("/destroy")
async def route_provision_private_cloud():
    return await service_destroy_private_cloud()

@na_private_router.get("/destroy_and_provision")
async def route_destroy_provision_private_cloud():
    return await service_destroy_and_provision_private_cloud()

@na_private_router.get("/provision")
async def route_provision_private_cloud():
    return await service_provision_private_cloud()

@na_private_router.get("/apply")
async def route_apply_private_cloud():
    return await service_apply_private_cloud()

@na_private_router.get("/configure")
async def route_configure_private_cloud():
    return await service_configure_private_cloud()

@na_private_router.get("/write_terraform_output")
async def route_write_terraform_output():
    return await service_write_terraform_output()
    
