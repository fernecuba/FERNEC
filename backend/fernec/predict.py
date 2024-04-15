import os
from fernec.models import ImageItem, ImagePrediction, VideoItem, VideoPrediction
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import base64
from tensorflow.keras.models import load_model
from keras.src.saving import serialization_lib
import numpy as np
from fernec.video_predictor import predict_video, print_prediction
import cv2

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
async def predict_video_endpoint(video_item: VideoItem) -> VideoPrediction:
    try:
        prediction = predict_video(video_item.video_path, video_item.model_name)

        return JSONResponse(status_code=200, content={
            "prediction": print_prediction(prediction)
        })
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/video_info")
async def process_video(request: Request):
    try:
        # Verifica si hay archivos en la solicitud
        form_data = await request.form()
        if "video_file" not in form_data:
            return JSONResponse(content={"message": "No se encontró el archivo de video"}, status_code=400)

        # Obtiene el archivo de video de la solicitud
        video_file = form_data["video_file"]

        # Lee el contenido del archivo de video
        contents = await video_file.read()

        # Guarda el archivo temporalmente
        with open("temp_video.mp4", "wb") as temp_video:
            temp_video.write(contents)

        # Lee el video con OpenCV
        cap = cv2.VideoCapture("temp_video.mp4")

        # Obtiene la duración del video
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        duration = frames / fps

        # Elimina el archivo temporal
        cap.release()
        cv2.destroyAllWindows()

        return JSONResponse(content={"duration": duration}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)