from pydantic import BaseModel

class ImageItem(BaseModel):
    image_base64: str

class ImagePrediction(BaseModel):
    predictions: list[float]
    emotion: str
