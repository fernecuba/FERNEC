from pydantic import BaseModel

class ImageItem(BaseModel):
    image_base64: str

class ImagePrediction(BaseModel):
    predictions: list[float]
    emotion: str

class VideoItem(BaseModel):
    video_path: str
    model_name: str

class VideoPrediction(BaseModel):
    prediction: list[str]
