from fastapi import APIRouter
from pydantic import BaseModel

from .service import *
from optimization_engine.cost_model.privateModel import privateCost_v1, privateCost_v2

# Private cloud
optimize_engine_router = APIRouter(
    prefix="/opt_eng",
    tags=["opt_eng"],
)

@optimize_engine_router.get("/")
async def root():
    return {"message": "This is the optimization engine"}

class OptimizeRequest(BaseModel):
    optimizer_strategy_name: str = "pymoo_v2"
    services_list: list = []
    cpu_usage_of_pods_in_other_ns: int = 150
    cpu_usage_of_ds_in_other_ns: int = 20
    private_cost_func: str = "privateCost_v1"

@optimize_engine_router.post("/get_nodes")
async def route_get_node_configuration(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    service_list = request_data.services_list
    cpu_usage_of_pods_in_other_ns = request_data.cpu_usage_of_pods_in_other_ns
    cpu_usage_of_ds_in_other_ns = request_data.cpu_usage_of_ds_in_other_ns
    private_cost_func = request_data.private_cost_func
    
    if (private_cost_func == "privateCost_v2" ):
        private_cost_func = privateCost_v2
    else:
        private_cost_func = privateCost_v1
        
    return await returnNodeConfiguration(optimizer_strategy_name, service_list, cpu_usage_of_pods_in_other_ns, cpu_usage_of_ds_in_other_ns, private_cost_func)

    
