from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class StatusResponse(GenericModel, Generic[DataT]):
    success: bool
    message: Optional[str] = None
    data: Optional[DataT] = None


class ImageItem(BaseModel):
    image_base64: str


class ImagePrediction(BaseModel):
    predictions: list[float]
    emotion: str


class VideoPrediction(BaseModel):
    prediction: list[str]
