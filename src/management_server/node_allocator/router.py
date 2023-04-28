from fastapi import APIRouter

from .service import provision_private_cloud
from .terraform.private_cloud.private_cloud_terraform import provision_private_cloud

node_allocator_router = APIRouter(
    prefix="/node_allocator",
    tags=["node_allocator"],
)

@node_allocator_router.get("/")
async def root():
    return {"message": "This is the node allocator router"}

@node_allocator_router.get("/provision_private_cloud")
async def route_provision_private_cloud():
    return await provision_private_cloud()