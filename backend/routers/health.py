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
    video_config = request.app.state.video_config
    models = request.app.state.models_names 

    return JSONResponse(status_code=200, content=jsonable_encoder({
        "video_config": video_config,
        "models": models
    }))
