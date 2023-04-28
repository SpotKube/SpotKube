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
    return await destroy_private_cloud()

@na_private_router.get("/destroy_and_provision")
async def route_provision_private_cloud():
    return await destroy_and_provision_private_cloud()

@na_private_router.get("/provision")
async def route_provision_private_cloud():
    return await provision_private_cloud()

@na_private_router.get("/apply")
async def route_apply_private_cloud():
    return await apply_private_cloud()
    
