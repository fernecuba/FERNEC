import os
import io
import uuid
import base64
import numpy as np

from PIL import Image
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from .models import ImageItem, ImagePrediction, VideoPrediction
from .video_predictor import predict_video, count_frames_per_emotion


router = APIRouter(prefix="/predict")

# TODO: this is good enough only for 1 worker
predictions = {}


@router.post('/image')
async def predict_image(request: Request, image_item: ImageItem) -> JSONResponse:
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
        predictions_result = request.app.state.cnn_model.predict(image).tolist()[0]
        prediction_class = np.argmax(predictions_result)
        emociones = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
        return JSONResponse(status_code=200, content={
            "predictions": predictions,
            "emotion": emociones[prediction_class]
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/{prediction_id}')
def get_predictions(prediction_id: str) -> JSONResponse:
    if prediction_id not in predictions.keys():
        return JSONResponse(content={"message": f"prediction with id {prediction_id} does not exist"}, status_code=404)
    if predictions[prediction_id] is None:
        return JSONResponse(content={"message": f"prediction with id {prediction_id} is not ready yet"},
                            status_code=202)
    return JSONResponse(content=predictions[prediction_id], status_code=200)


@router.post('/video')
async def predict_video_endpoint(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
    try:
        # Verify there is a file in the request
        form_data = await request.form()
        if "video_file" not in form_data:
            return JSONResponse(content={"message": "Couldn't find video file"}, status_code=400)

        video_file = form_data["video_file"]

        video_format = os.path.splitext(video_file.filename)[-1].lower()

        contents = await video_file.read()

        # Save the video file temporarily
        temp_video_path = "temp_video" + video_format
        with open(temp_video_path, "wb") as temp_video:
            temp_video.write(contents)

        unique_id = str(uuid.uuid4())
        feature_extractor = request.app.state.feature_extractor
        rnn =  request.app.state.rnn_model
        rnn_binary = request.app.state.rnn_binary_model
        cfg = request.app.state.video_config
        background_tasks.add_task(predict_video_async, temp_video_path, feature_extractor, rnn, rnn_binary, unique_id, cfg)
        # i.e. prediction is calculating
        predictions[unique_id] = None
        return JSONResponse(status_code=202, content={"uuid": unique_id})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def predict_video_async(temp_video_path, cnn_model, rnn_model, rnn_binary_model, unique_id, video_config):
    prediction, prediction_binary = predict_video(temp_video_path, cnn_model, rnn_model, rnn_binary_model, video_config)
    result = count_frames_per_emotion(prediction, prediction_binary)
    predictions[unique_id] = result
    print(f"prediction is done for unique_id {unique_id}")
