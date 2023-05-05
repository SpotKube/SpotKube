from fastapi import APIRouter

from .service import *

# Private cloud
helm_router_private = APIRouter(
    prefix="/helm_service/private",
    tags=["helm_service"],
)

@helm_router_private.get("/")
async def root():
    return {"message": "This is the helm service private cloud router"}

@helm_router_private.get("/deploy")
async def deploy_helm_charts():
    return await deploy_helm_charts()

@helm_router_private.get("/uninstall")
async def uninstall():
    return await uninstall_helm_charts()
    
