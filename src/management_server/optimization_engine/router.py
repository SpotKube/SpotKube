from fastapi import APIRouter
from pydantic import BaseModel

from .service import *

# Private cloud
optimize_engine_router = APIRouter(
    prefix="/opt_eng",
    tags=["opt_eng"],
)

@optimize_engine_router.get("/")
async def root():
    return {"message": "This is the optimization engine"}

class OptimizeRequest(BaseModel):
    optimizer_strategy_name: str | None = None 

@optimize_engine_router.post("/get_nodes")
async def route_get_node_configuration(request_data: OptimizeRequest):
    optimizer_strategy_name = request_data.optimizer_strategy_name
    if not optimizer_strategy_name:
        #set default optimizer strategy
        optimizer_strategy_name = "greedy_v2"
    
    return await returnNodeConfiguration(optimizer_strategy_name)

    
