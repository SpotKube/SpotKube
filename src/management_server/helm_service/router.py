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
async def deploy_helm_charts():
    return await deploy_helm_charts()

@helm_router.get("/uninstall")
async def uninstall_helm_charts():
    return await uninstall_helm_charts()
    
