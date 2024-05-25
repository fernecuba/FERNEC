import os
import cv2
import math
import numpy as np

from keras.models import Sequential, load_model

from ..preprocessing.frames_generator.strategy.videos_processor.videos import get_frames_from_video
from ..preprocessing.frames_generator.utils import create_folder_if_not_exists, clean_folder

# Temp path to save the frames extracted from the video
TMP_FRAMES_PATH = "./temp/frames/"
# In this path we will save the frames that are ready to be predicted
TMP_FRAMES_READY_PATH = "temp/frames_ready/"

# TODO: Move this to a config file?
HEIGHT = 112
WIDTH = 112
CHANNELS = 3
HEIGHT_POSITION = 2
WIDTH_POSITION = 3
Y = 0
X = 1
MAX_SEQ_LENGTH = 10
NUM_FEATURES = 1024
FRAMES_ORDER_MAGNITUDE = 5
FACE_BATCH_SIZE = 20


def prepare_frames(model_cnn_path, verbose=False):
    cnn_model = load_model(model_cnn_path)
    
    model = Sequential()
    for layer in cnn_model.layers[:-1]: # go through until last layer
        model.add(layer)

    files = os.listdir(TMP_FRAMES_READY_PATH)
    iterations = math.ceil(len(files) / MAX_SEQ_LENGTH)

    frames_features = np.zeros(shape=(iterations, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")
    frames_mask = np.ones(shape=(iterations, MAX_SEQ_LENGTH))

    for iteration in range(0, iterations):
        idx = 0

        for i in range(0, MAX_SEQ_LENGTH):
            frame_path = TMP_FRAMES_READY_PATH + f"{str(i + (iteration * MAX_SEQ_LENGTH)).zfill(FRAMES_ORDER_MAGNITUDE)}.jpg"

            if verbose:
                print("Leo: " + frame_path)

            if os.path.isfile(frame_path):
                
                frame = cv2.imread(frame_path)
                img = np.reshape(frame, (HEIGHT, WIDTH, CHANNELS))
                img = np.expand_dims(img, axis=0)
        
                prediction = model.predict(img, verbose=0) # shape (1, num_features)
                assert len(prediction[0]) == NUM_FEATURES, 'Error features'
        
                frames_features[iteration, idx] = prediction[0]
                
            else:
                
                if verbose:
                    print("File not found, filling mask")
                frames_mask[iteration, idx] = 0
                
            idx += 1

    return [frames_features, frames_mask]


def predict_video(video_path, model_cnn_path, model_rnn_path):

    create_folder_if_not_exists(TMP_FRAMES_READY_PATH)
    clean_folder(TMP_FRAMES_READY_PATH)

    get_frames_from_video(
            video_path,
            TMP_FRAMES_READY_PATH,
            FACE_BATCH_SIZE,
            CHANNELS,
            (HEIGHT, WIDTH),
            FRAMES_ORDER_MAGNITUDE,
            faces_only=True
    )

    model_imported = load_model(model_rnn_path)
    print("Loaded model from path " + model_rnn_path)

    frames_to_predict = prepare_frames(model_cnn_path)
    predictions = model_imported.predict(frames_to_predict)

    return predictions


# We are not going to use this one to return the predictions in the endpoint for now.
def print_prediction(predictions):
    """
    Prints the predicted labels for each frame in a video.

    Args:
        predictions (list): A list of predictions for each frame in the video.

    Returns:
        list: A list of strings representing the frame number and the predicted label for each frame.
    """
    class_vocab = [
        "Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"
    ]
    print(class_vocab)
    results = []

    len_files = len(os.listdir(TMP_FRAMES_READY_PATH))
    i = 0
    
    for prediction in predictions:
    
        for result in prediction:
            result_argmax = result.argmax()
            result_label = class_vocab[result_argmax]

            # TODO: We should find a better way to avoid the masked results.
            if i < len_files:
                results.append(f"frame {i} - result {result_label}")
            i += 1
    
    return results


def count_frames_per_emotion(predictions):
    """
    Counts the number of frames per emotion in the given predictions.

    Args:
        predictions (list): A list of predictions, where each prediction is a list of emotion probabilities.

    Returns:
        dict: A dictionary containing the total number of frames and a list of emotions with their respective frame counts.
            Example:
            {
                "total_frames": 100,
                "emotions": [
                    {"label": "Neutral", "total_frames": 20},
                    {"label": "Anger", "total_frames": 10},
                    {"label": "Disgust", "total_frames": 5},
                    ...
                ]
            }
    """
    class_vocab = ["Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise"]
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

    total_frames = sum(emotion_counts.values())
    emotions_list = [{"label": emotion, "total_frames": count} for emotion, count in emotion_counts.items()]

    result = {
        "total_frames": total_frames,
        "emotions": emotions_list
    }

    return result
