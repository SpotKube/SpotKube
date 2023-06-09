from fastapi import FastAPI

# Import routers
from node_allocator.router_private_cloud import na_private_router 
from node_allocator.router_aws_cloud import na_aws_router
from helm_service.router import helm_router
from optimization_engine.router import optimize_engine_router
from logs.router import log_router
from router import main_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include routers
app.include_router(na_private_router)
app.include_router(na_aws_router)
app.include_router(helm_router)
app.include_router(optimize_engine_router)
app.include_router(main_router)
app.include_router(log_router)
