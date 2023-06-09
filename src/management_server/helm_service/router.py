from fastapi import APIRouter

from .service import *

helm_router = APIRouter(
    prefix="/helm_service",
    tags=["helm_service"],
)

@helm_router.get("/")
async def root():
    return {"message": "This is the helm service router"}

@helm_router.get("/deploy_private")
async def route_deploy_helm_chart():
    return await deploy_helm_charts(True)

@helm_router.get("/deploy_aws")
async def route_deploy_helm_chart():
    return await deploy_helm_charts()

    
