from item import Item, ImageItem, ImagePrediction
from typing import Union
from fastapi import FastAPI
from PIL import Image
import io
import base64
from tensorflow.keras.models import load_model
from keras.src.saving import serialization_lib
import numpy as np

#Need to load model
serialization_lib.enable_unsafe_deserialization()

app = FastAPI(title='FERNEC API')

model = load_model("./models/cotatest.keras")

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


@app.post('/image/predict')
async def predict_image(image_item: ImageItem) -> ImagePrediction:
    try:
        print('HERERE')
        # Decodificar la imagen Base64
        image_data = base64.b64decode(image_item.image_base64)
        # Convertir los datos de la imagen en un objeto de imagen
        image = Image.open(io.BytesIO(image_data))
        # Preprocesar la imagen para que coincida con el formato esperado por el modelo
        image = image.resize((224, 224))  # Ajustar tam
        image = np.array(image) / 255.0  # Normaliza los valores de píxeles
        image = np.expand_dims(image, axis=0)  # Agrega una dimensión de lote

        # Realizar la predicción utilizando el modelo cargado
        predictions = model.predict(image).tolist()
        prediction_class = np.argmax(predictions)
        emociones = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
        return {
            "predictions": predictions,
            "emotion": emociones[prediction_class]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))