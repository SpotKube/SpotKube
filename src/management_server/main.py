from fastapi import FastAPI

# Import routers
from node_allocator.router import node_allocator_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include routers
app.include_router(node_allocator_router)