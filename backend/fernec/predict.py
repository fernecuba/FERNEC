from fernec.models import ImageItem, ImagePrediction
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from tensorflow.keras.models import load_model
from keras.src.saving import serialization_lib
import numpy as np

router = APIRouter(prefix="/predict")

# Needed to load model
serialization_lib.enable_unsafe_deserialization()
# Load model
# TO DO: move path to env variable
model = load_model("./fernec/ia_models/cotatest.keras")

@router.post('/image')
async def predict_image(image_item: ImageItem) -> ImagePrediction:
    try:
        # Decodificar la imagen Base64
        image_data = base64.b64decode(image_item.image_base64)
        # Convertir los datos de la imagen en un objeto de imagen
        image = Image.open(io.BytesIO(image_data))
        # Preprocesar la imagen para que coincida con el formato esperado por el modelo
        image = image.resize((224, 224))  # Ajustar tam

        image = np.expand_dims(image, axis=0)  # Agrega una dimensión de lote

        # TO DO: cut face from image

        # Realizar la predicción utilizando el modelo cargado
        predictions = model.predict(image).tolist()[0]
        prediction_class = np.argmax(predictions)
        emociones = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
        return JSONResponse(status_code=200, content={
            "predictions": predictions,
            "emotion": emociones[prediction_class]
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))