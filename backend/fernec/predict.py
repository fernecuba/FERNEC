import os
from fernec.models import ImageItem, ImagePrediction, VideoPrediction
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from tensorflow.keras.models import load_model
from keras.src.saving import serialization_lib
import numpy as np
from fernec.video_predictor import predict_video, print_prediction

router = APIRouter(prefix="/predict")

# Needed to load model
serialization_lib.enable_unsafe_deserialization()
# Load model
model_path = os.getenv('MODEL_PATH', './fernec/ia_models/cotatest.keras')
model = load_model(model_path)

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
    
@router.post('/video')
async def predict_video_endpoint(request: Request) -> VideoPrediction:
    try:
        # Verify there is a file in the request
        form_data = await request.form()
        if "video_file" not in form_data:
            return JSONResponse(content={"message": "Couldn't find video file"}, status_code=400)

        video_file = form_data["video_file"]

        contents = await video_file.read()

        # Save the video file temporarily
        with open("temp_video.mp4", "wb") as temp_video:
            temp_video.write(contents)

        prediction = predict_video("temp_video.mp4", "model4_rnn_poc3.keras")

        return JSONResponse(status_code=200, content={
            "prediction": print_prediction(prediction)
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    