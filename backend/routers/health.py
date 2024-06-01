from fastapi import APIRouter, Request
from .models import StatusResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/health")
def healthcheck() -> StatusResponse:
    return StatusResponse(success=True, message="ok")


@router.get('/config/video')
def get_video_config(request: Request):
    cfg = request.app.state.video_config
    return JSONResponse(status_code=200, content=jsonable_encoder(cfg))
