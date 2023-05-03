from fastapi import APIRouter

from .service import *

# Private cloud
helm_router = APIRouter(
    prefix="/helm_service/private",
    tags=["helm_service"],
)

@helm_router.get("/")
async def root():
    return {"message": "This is the helm service private cloud router"}

@helm_router.get("/deploy")
async def route_provision_private_cloud():
    return await deploy_helm_charts()

    
