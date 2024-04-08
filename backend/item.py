from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class ImageItem(BaseModel):
    image_base64: str

class ImagePrediction(BaseModel):
    predictions: list[str]
    emotion: str