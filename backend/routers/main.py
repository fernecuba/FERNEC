from fastapi import APIRouter

from .health import router as health_router
from .predict import router as predict_router
from .messaging import router as messaging_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(predict_router)
v1_router.include_router(health_router)
v1_router.include_router(messaging_router)
