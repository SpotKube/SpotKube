from fastapi import APIRouter

from .service import *

dashboard_router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)

@dashboard_router.get("/spot-instances")
async def get_running_spot_instances():
    spot_isntances = get_spot_instances()
    return {"message": spot_isntances, "status": 200}
