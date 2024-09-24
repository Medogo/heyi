from fastapi import APIRouter
from app.api.v1.endpoints import linkedin
from app.api.v1.endpoints import utilisateurs

api_router = APIRouter()
api_router.include_router(linkedin.router, prefix="/linkedin", tags=["linkedin"])
api_router.include_router(utilisateurs.router, prefix="/utilisateurs", tags=["utilisateurs"])