from fastapi import FastAPI

# Import routers
from node_allocator.router_private_cloud import na_private_router 
from helm_service.router import helm_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include routers
app.include_router(na_private_router)
app.include_router(helm_router)