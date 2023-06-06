from fastapi import APIRouter

from service import *

# Private cloud
main_router = APIRouter(
    prefix="",
    tags=["Management Server"],
)

@main_router.get("/")
async def root():
    return {"message": "This is the management server main_router"}

@main_router.post("/startup_private_cloud")
async def route_startup_private_cloud():
    return await startUpPrivateCloud()

@main_router.post("/update_private_cloud")
async def route_update_private_cloud():
    return await updatePrivateCloud() 

@main_router.post("/startup_aws_cloud")
async def route_startup_aws_cloud():
    return await startUpPrivateCloud()

@main_router.post("/update_aws_cloud")
async def route_update_aws_cloud():
    return await updateAwsCloud() 
