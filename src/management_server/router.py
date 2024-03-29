from fastapi import APIRouter
from pydantic import BaseModel

from optimization_engine.cost_model.privateModel import privateCost_v1, privateCost_v2

from service import *


    
# Private cloud
main_router = APIRouter(
    prefix="",
    tags=["Management Server"],
)

class OptimizeRequest(BaseModel):
    optimizer_strategy_name: str = "pymoo_v2"
    services_list: list = []
    cpu_usage_of_pods_in_other_ns: int = 150
    cpu_usage_of_ds_in_other_ns: int = 20
    private_cost_func: str = "privateCost_v1"

@main_router.get("/")
async def root():
    return {"message": "This is the management server main_router"}

@main_router.post("/startup_private_cloud")
async def route_startup_private_cloud(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    cpu_usage_of_pods_in_other_ns = request_data.cpu_usage_of_pods_in_other_ns
    cpu_usage_of_ds_in_other_ns = request_data.cpu_usage_of_ds_in_other_ns
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
    return await startUpPrivateCloud(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func)

@main_router.post("/update_private_cloud")
async def route_update_private_cloud(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    cpu_usage_of_pods_in_other_ns = request_data.cpu_usage_of_pods_in_other_ns
    cpu_usage_of_ds_in_other_ns = request_data.cpu_usage_of_ds_in_other_ns
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
    return await updatePrivateCloud(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func) 

@main_router.post("/startup_aws_cloud")
async def route_startup_aws_cloud(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    cpu_usage_of_pods_in_other_ns = request_data.cpu_usage_of_pods_in_other_ns
    cpu_usage_of_ds_in_other_ns = request_data.cpu_usage_of_ds_in_other_ns
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
    return await startUpAwsCloud(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func)

    
@main_router.post("/update_aws_cloud")
async def route_update_aws_cloud(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    cpu_usage_of_pods_in_other_ns = request_data.cpu_usage_of_pods_in_other_ns
    cpu_usage_of_ds_in_other_ns = request_data.cpu_usage_of_ds_in_other_ns
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
    return await updateAwsCloud(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func) 
