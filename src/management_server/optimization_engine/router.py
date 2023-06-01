from fastapi import APIRouter

from .optimizer.optimizerMain import returnNodeConfiguration

# Private cloud
optimize_engine_router = APIRouter(
    prefix="/helm_service/private",
    tags=["helm_service"],
)

@optimize_engine_router.get("/")
async def root():
    return {"message": "This is the optimization engine"}

@optimize_engine_router.get("/get_nodes")
async def route_get_node_configuration():
    return await returnNodeConfiguration()

    
