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


class VideoConfig(BaseModel):
    MAX_SEQ_LENGTH: int
    FRAMES_ORDER_MAGNITUDE: int
    HEIGHT: int
    WIDTH: int
    CHANNELS: int = 3
    NUM_FEATURES: int
    FACE_BATCH_SIZE: int


class EmailConfig(BaseModel):
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int


class Email(BaseModel):
    recipients: list[str]
    subject: str
    body: str
