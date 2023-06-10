from fastapi import APIRouter
from pydantic import BaseModel

from optimization_engine.cost_model.privateModel import privateCost_v1, privateCost_v2

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
    return await startUpAwsCloud()

class OptimizeRequest(BaseModel):
    optimizer_strategy_name: str = "pymoo_v2"
    services_list: list = []
    allocated_nodes: list = []
    private_cost_func: str = "privateCost_v1"
    
@main_router.post("/update_aws_cloud")
async def route_update_aws_cloud(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    allocated_nodes = request_data.allocated_nodes
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
    return await updateAwsCloud(optimizer_strategy_name, service_list, allocated_nodes, private_cost_func) 
