import os
import cv2
import math
import numpy as np
from loguru import logger
from preprocessing.frames_generator.strategy.videos_processor.videos import get_frames_from_video, frames_to_seconds
from preprocessing.frames_generator.utils import create_folder_if_not_exists, clean_folder
from .models import VideoConfig

# Temp path to save the frames extracted from the video
TMP_FRAMES_PATH = "./temp/frames/"
# In this path we will save the frames that are ready to be predicted
TMP_FRAMES_READY_PATH = "temp/frames_ready/"


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


def count_frames_per_emotion(predictions, predictions_binary, fps):
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

    # emotions_list = calculate_emotion_counts(predictions, class_vocab, fps)
    # emotions_list_binary = calculate_emotion_counts(predictions_binary, class_vocab_binary, fps)

    emotions_list, emotions_list_binary, total_frames = consolidate_results(predictions, predictions_binary, fps)

    result = {
        "total_frames": total_frames,
        "total_seconds": frames_to_seconds(total_frames, fps),
        "fps": fps,
        "emotions": emotions_list,
        "emotions_binary": emotions_list_binary,
    }

    return result

def consolidate_results(predictions, predictions_binary, fps):
    class_vocab = ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
    class_vocab_binary = ["Negative", "Positive"]

    emotions_list = calculate_emotion_counts(predictions, class_vocab, fps)
    emotions_list_binary = calculate_emotion_counts(predictions_binary, class_vocab_binary, fps)
    
    # Total frames
    total_frames = sum([emotion["total_frames"] for emotion in emotions_list])
    total_frames_binary = sum([emotion["total_frames"] for emotion in emotions_list_binary])
    
    # Calculate percentages
    percentage_negative_binary = next(emotion["total_frames"] for emotion in emotions_list_binary if emotion["label"] == "Negative") / total_frames_binary * 100

    # Determine the final result based on the binary model percentage
    if percentage_negative_binary >= 60:
        # Video is mostly negative
        result_emotions = [emotion for emotion in emotions_list if emotion["label"] in ["Anger", "Disgust", "Fear", "Sadness", "Surprise"]]
        result_emotions_binary = emotions_list_binary
        total_frames = sum([emotion["total_frames"] for emotion in result_emotions_binary])
    else:
        # Translate 7-emotions results to binary results
        result_emotions = emotions_list
        negative_emotions = sum([emotion["total_frames"] for emotion in emotions_list if emotion["label"] in ["Anger", "Disgust", "Fear", "Sadness", "Surprise"]])
        positive_emotions = sum([emotion["total_frames"] for emotion in emotions_list if emotion["label"] in ["Neutral", "Happiness"]])
        total_frames = sum([emotion["total_frames"] for emotion in result_emotions])
        
        result_emotions_binary = [
            {"label": "Negative", "total_frames": negative_emotions, "total_seconds": frames_to_seconds(negative_emotions, fps)},
            {"label": "Positive", "total_frames": positive_emotions, "total_seconds": frames_to_seconds(positive_emotions, fps)}
        ]

    return result_emotions, result_emotions_binary, total_frames


def calculate_emotion_counts(predictions, class_vocab, fps):
    emotion_counts = {emotion: 0 for emotion in class_vocab}
    len_files = len(os.listdir(TMP_FRAMES_READY_PATH))
    i = 0
    for prediction in predictions:
        for result in prediction:
            result_argmax = np.argmax(result)
            result_label = class_vocab[result_argmax]
            
            # TODO: We should find a better way to avoid the masked results.
            if i < len_files:
                emotion_counts[result_label] += 1
            i += 1

    emotions_list = [{"label": emotion, "total_frames": frames, "total_seconds": frames_to_seconds(frames, fps)}
                     for emotion, frames in emotion_counts.items()]
    return emotions_list
