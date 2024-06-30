import os
import io
import base64
import numpy as np
import json
from loguru import logger
from PIL import Image
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from resources.results_email import results_email_body
from .models import ImageItem
from .video_predictor import predict_video, count_frames_per_emotion
from .messaging import _send_email

router = APIRouter(prefix="/predict")


@router.post('/image')
async def predict_image(request: Request, image_item: ImageItem) -> JSONResponse:
    try:
        image_data = base64.b64decode(image_item.image_base64)
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((request.app.state.video_config.WIDTH, request.app.state.video_config.HEIGHT))

        predictions_result = request.app.state.cnn_model.predict(image).tolist()[0]
        prediction_class = np.argmax(predictions_result)
        emociones = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise']
        return JSONResponse(status_code=200, content={
            "predictions": predictions_result,
            "emotion": emociones[prediction_class]
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post('/video')
async def predict_video_endpoint(
    request: Request, 
    background_tasks: BackgroundTasks
) -> JSONResponse:
    try:
        form_data = await request.form()
        # Check file exists
        if "video_file" not in form_data:
            raise HTTPException(status_code=400, detail="Couldn't find video file")

        user_email = str(form_data["email"])
        video_file = form_data["video_file"]
        video_format = os.path.splitext(video_file.filename)[-1].lower()

        contents = await video_file.read()

        # Save the video file temporarily
        temp_video_path = "temp_video" + video_format
        logger.info(f"video_format is {video_format}")
        with open(temp_video_path, "wb") as temp_video:
            temp_video.write(contents)

        background_tasks.add_task(predict_video_task, temp_video_path, user_email, request, background_tasks)
        return JSONResponse(status_code=202, content={})

    except HTTPException as e:
        logger.error(f"HTTPException in predict_video_endpoint {e}")
        raise e
    except Exception as e:
        logger.error(f"exception in predict_video_endpoint {e}")
        raise HTTPException(status_code=500, detail=str(e))


def encode_results(results):
    res = json.dumps(results)
    return base64.b64encode(res.encode("utf-8")).decode("utf-8")


def predict_video_task(temp_video_path: str, user_email: str | None, request: Request,
                       background_tasks: BackgroundTasks):
    try:
        feature_extractor = request.app.state.feature_extractor
        rnn_model = request.app.state.rnn_model
        feature_extractor_binary = request.app.state.feature_binary_extractor
        rnn_binary_model = request.app.state.rnn_binary_model
        video_config = request.app.state.video_config
        logger.info("Preparing frames")
        prediction, prediction_binary, fps, duration = predict_video(temp_video_path, feature_extractor, rnn_model,
                                                                     feature_extractor_binary, rnn_binary_model,
                                                                     video_config)

        logger.info("Counting frames")
        result = count_frames_per_emotion(prediction, prediction_binary, fps, duration, video_config)

        logger.success(f"Prediction is done. Result is {result}")
        if user_email:
            background_tasks.add_task(send_email_with_prediction_results, result, user_email, request)

    except Exception as e:
        logger.error(f"exception in predict_video_async {e}")
        raise e


def send_email_with_prediction_results(result, user_email: str, request: Request):
    email_config = request.app.state.email_config
    logger.info("about to send prediction results!", request.client.host)
    recipients = [user_email]
    result_encoded = encode_results(result)
    logger.debug(f"Results hashed: {result_encoded}")
    url = f"{request.headers.get('origin')}/results/{result_encoded}"
    body = results_email_body.format(url)
    _send_email(recipients, "fernec results", body, email_config)
