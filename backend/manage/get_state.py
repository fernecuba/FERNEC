from fastapi import APIRouter
from shared.models import StatusResponse

router = APIRouter()

@router.get("/health")
def healthcheck() -> StatusResponse:
    return StatusResponse(success=True, message="ok")
