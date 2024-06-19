import os
import io
import uuid
import base64
import numpy as np
import json
from loguru import logger
from PIL import Image
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from .models import ImageItem
from .video_predictor import predict_video, count_frames_per_emotion
from .messaging import _send_email

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
async def predict_video_endpoint(
    request: Request, 
    background_tasks: BackgroundTasks
) -> JSONResponse:
    try:
        # Verify there is a file in the request
        form_data = await request.form()
        if "video_file" not in form_data:
            return JSONResponse(content={"message": "Couldn't find video file"}, status_code=400)

        user_email = str(form_data['email'])
        video_file = form_data["video_file"]

        video_format = os.path.splitext(video_file.filename)[-1].lower()

        contents = await video_file.read()

        # Save the video file temporarily
        temp_video_path = "temp_video" + video_format
        logger.info(f"video_format is {video_format}")
        with open(temp_video_path, "wb") as temp_video:
            temp_video.write(contents)

        unique_id = str(uuid.uuid4())
        background_tasks.add_task(predict_video_async, temp_video_path, unique_id, user_email, request,
                                  background_tasks)
        # i.e. prediction is calculating
        predictions[unique_id] = None
        return JSONResponse(status_code=202, content={"uuid": unique_id})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def encode_results(results):
    res = json.dumps(results)
    return base64.b64encode(res.encode("utf-8")).decode("utf-8")


def predict_video_async(temp_video_path: str, unique_id: str, user_email: str | None,  request: Request,
                        background_tasks: BackgroundTasks):
    feature_extractor = request.app.state.feature_extractor
    rnn_model = request.app.state.rnn_model
    feature_extractor_binary = request.app.state.feature_binary_extractor
    rnn_binary_model = request.app.state.rnn_binary_model
    video_config = request.app.state.video_config
    logger.info('Prepearing frames')
    prediction, prediction_binary, fps = predict_video(temp_video_path, feature_extractor, rnn_model,
                                                       feature_extractor_binary, rnn_binary_model, video_config)

    logger.info('Counting frames')
    result = count_frames_per_emotion(prediction, prediction_binary, fps)
    logger.success(f"result is {result}")
    predictions[unique_id] = result
    logger.success(f"Prediction is done for unique_id {unique_id}")
    if user_email:
        background_tasks.add_task(send_email_with_prediction_results, result, user_email, request)


def send_email_with_prediction_results(result, user_email: str, request: Request):
    email_config = request.app.state.email_config
    logger.info("about to send prediction results!", request.client.host)
    recipients = [user_email]
    result_encoded = encode_results(result)
    logger.debug(f"Results hashed: {result_encoded}")
    url = f"{request.headers.get('origin')}/results/{result_encoded}"
    body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333; font-size: 18px;">
                    <div style="text-align: center; padding: 20px;">
                        <img src="cid:logo" alt="FERNEC Logo" style="width: 200px;">
                    </div>
                    <div style="margin: 20px; text-align: center;">
                        <h2 style="font-size: 24px;">Dear User,</h2>
                        <p style="font-size: 20px;">We are pleased to inform you that your results are ready.</p>
                        <p style="font-size: 20px;">Please click the link below to view them:</p>
                        <a href="{url}" style="display: inline-block; padding: 12px 24px; background-color: #007BFF; color: #fff; text-decoration: none; border-radius: 5px; font-size: 20px;">View Results</a>
                        <p style="font-size: 20px;">Sincerely,<br>The FERNEC Team</p>
                    </div>
                </body>
            </html>
            """
    _send_email(recipients, "fernec results", body, email_config)
