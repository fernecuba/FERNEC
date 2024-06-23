import os
import cv2
import math
import numpy as np
from loguru import logger
from preprocessing.frames_generator.strategy.videos_processor.videos import get_frames_from_video, frames_to_seconds
from preprocessing.frames_generator.utils import create_folder_if_not_exists, clean_folder
from .models import VideoConfig
from .results_consolidation import consolidate_results

# Temp path to save the frames extracted from the video
TMP_FRAMES_PATH = "./temp/frames/"
# In this path we will save the frames that are ready to be predicted
TMP_FRAMES_READY_PATH = "temp/frames_ready/"

BINARY_ACCEPTANCE_THRESHOLD = 60


def prepare_frames(feature_extractor, cfg: VideoConfig):
    files = os.listdir(TMP_FRAMES_READY_PATH)
    iterations = math.ceil(len(files) / cfg.MAX_SEQ_LENGTH)

    frames_features = np.zeros(shape=(iterations, cfg.MAX_SEQ_LENGTH, cfg.NUM_FEATURES), dtype="float32")
    frames_mask = np.ones(shape=(iterations, cfg.MAX_SEQ_LENGTH))

    for iteration in range(0, iterations):
        idx = 0
        for i in range(0, cfg.MAX_SEQ_LENGTH):
            frame_path = (TMP_FRAMES_READY_PATH +
                          f"{str(i + (iteration * cfg.MAX_SEQ_LENGTH)).zfill(cfg.FRAMES_ORDER_MAGNITUDE)}.jpg")
            logger.debug("Read: " + frame_path)
            if os.path.isfile(frame_path):
                frame = cv2.imread(frame_path)
                img = np.reshape(frame, (cfg.HEIGHT, cfg.WIDTH, cfg.CHANNELS))
                img = np.expand_dims(img, axis=0)

                # shape (1, num_features)
                prediction = feature_extractor.predict(img, verbose=0)
                assert len(prediction[0]) == cfg.NUM_FEATURES, 'Error features'
                frames_features[iteration, idx] = prediction[0]
            else:
                logger.debug("File not found, filling mask")
                frames_mask[iteration, idx] = 0
                
            idx += 1

    return [frames_features, frames_mask]


def predict_video(video_path, feature_extractor, rnn_model, feature_binary_extractor, rnn_binary_model,
                  cfg: VideoConfig):
    create_folder_if_not_exists(TMP_FRAMES_READY_PATH)
    clean_folder(TMP_FRAMES_READY_PATH)

    _, fps = get_frames_from_video(
        video_path,
        TMP_FRAMES_READY_PATH,
        cfg.FACE_BATCH_SIZE,
        cfg.CHANNELS,
        (cfg.HEIGHT, cfg.WIDTH),
        cfg.FRAMES_ORDER_MAGNITUDE,
        faces_only=True
    )

    frames_to_predict = prepare_frames(feature_extractor, cfg)
    frames_to_predict_binary = prepare_frames(feature_binary_extractor, cfg)

    predictions = rnn_model.predict(frames_to_predict)
    predictions_binary = rnn_binary_model.predict(frames_to_predict_binary)

    return [predictions, predictions_binary, fps]


def count_frames_per_emotion(predictions, predictions_binary, fps, video_config):
    """
    Counts the number of frames per emotion in the given predictions.

    Args:
        predictions (list): A list of predictions, where each prediction is a list of emotion probabilities.
        predictions_binary (list): A list of predictions, where each prediction is a list of emotion probabilities for
            binary model.
        fps (int): frames per second
    Returns:
        dict: A dictionary containing the total number of frames and a list of emotions with their respective frame counts.
            Example:
            {
                "total_frames": 100,
                "emotions": [
                    {"label": "Neutral", "total_frames": 20, "seconds": 2},
                    {"label": "Anger", "total_frames": 10, "seconds": 1},
                    {"label": "Disgust", "total_frames": 5, "seconds": 1},
                    ...
                ]
                "emotions_binary": [
                    {"label": "Negative", "total_frames": 30, "seconds": 3},
                    {"label": "Positive", "total_frames": 70, "seconds": 7}
                ]
            }
    """
    emotions_list, emotions_list_binary, total_frames = consolidate_results(predictions, predictions_binary,
                                                                            len(os.listdir(TMP_FRAMES_READY_PATH)), fps,
                                                                            video_config, BINARY_ACCEPTANCE_THRESHOLD)

    result = {
        "total_frames": total_frames,
        "total_seconds": frames_to_seconds(total_frames, fps),
        "fps": fps,
        "emotions": emotions_list,
        "emotions_binary": emotions_list_binary,
    }

    return result
