import os
import cv2
import shutil
import math
import pandas as pd
import numpy as np
from PIL import Image
from facenet_pytorch import MTCNN as facenet_MTCNN
from keras.models import Sequential, load_model

# Temp path to save the frames extracted from the video
TMP_FRAMES_PATH = "./temp/frames/"
# In this path we will save the frames that are ready to be predicted
TMP_FRAMES_READY_PATH = "temp/frames_ready/"

HEIGHT = 112
WIDTH = 112
CHANNELS = 3
HEIGHT_POSITION = 2
WIDTH_POSITION = 3
Y = 0
X = 1
MAX_SEQ_LENGTH = 10
NUM_FEATURES = 1024


def clean_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("La ruta especificada no es una carpeta.")

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)


def split_video_into_frames(video_path, target_fps=23):
    # Open the video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    frame_rate = int(vidcap.get(cv2.CAP_PROP_FPS))
    frame_interval = int(frame_rate / target_fps)  # Intervalo para mantener la tasa de fotogramas deseada
    
    # Create output folder if it doesn't exist
    if not os.path.exists(TMP_FRAMES_PATH):
        os.makedirs(TMP_FRAMES_PATH)

    clean_folder(TMP_FRAMES_PATH)
    
    # Extract the frames
    while success:
        # Save frame in the output folder
        if count % frame_interval == 0:  # Only save frames at the desired rate
            frame_path = os.path.join(TMP_FRAMES_PATH, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, image)  # Save frame as JPG file
        success, image = vidcap.read()  # Read next frame
        count += 1

    # Close the video
    vidcap.release()


def get_boxes_from_face_detection(face_detection):
    boxes = []
    for face in face_detection:
        if face is not None and len(face) != 0:
            boxes.append(face[0])
        else:
            boxes.append(face)
    return boxes


def crop_image(image, bounding_box, verbose=False):
    cropped_image = image.crop((bounding_box[Y], bounding_box[X], bounding_box[HEIGHT_POSITION], bounding_box[WIDTH_POSITION]))
    if verbose:
        print(cropped_image.size)
    return cropped_image


def generate_image_pixels(frame, box, output_folder, verbose=False):
    # frame to image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    if CHANNELS == 1:
        image = image.convert('L') 

    if box is not None:
        # get boxes
        if len(box) != 0:
            if verbose:
                print(f"There is a box to crop: {box}")
            # Crop image to keep only the face
            cropped_image = crop_image(image, box, verbose)
            # Resize the cropped image to 48x48
            resized_image = cropped_image.resize((HEIGHT, WIDTH))
            # Save the resized image to the output folder
            output_path = os.path.join(output_folder, f"face_{len(os.listdir(output_folder))}.jpg")
            resized_image.save(output_path)
            if verbose:
                print(f"Saved image to {output_path}")
        else:
            print("No box detected for cropping")


def custom_sort(file_name):
    return int(file_name.split('_')[1].split('.')[0])


def process_frames(frames_path, frames_ready_path, batch_size=20, verbose=False):
    detector = facenet_MTCNN()

    if not os.path.exists(frames_ready_path):
        os.makedirs(frames_ready_path)

    clean_folder(frames_ready_path)
    
    image_files = sorted(os.listdir(frames_path), key=custom_sort)

    if verbose:
        print("Printing list of image files")
        for element in image_files:
            print(element)

    # Procesar por lotes
    for i in range(0, len(image_files), batch_size):
        batch_files = image_files[i:i+batch_size]  # Obtener los nombres de archivo para el lote actual
        raw_frames = []
    
        # Leer los fotogramas del lote actual
        for filename in batch_files:
            frame_path = os.path.join(frames_path, filename)
            frame = cv2.imread(frame_path)
            raw_frames.append(frame)
    
        # Detectar caras en los fotogramas del lote
        detected = detector.detect(raw_frames)
        boxes = get_boxes_from_face_detection(detected[0])
    
        # Procesar cada fotograma del lote
        for j, (frame, box) in enumerate(zip(raw_frames, boxes)):
            generate_image_pixels(frame, box, frames_ready_path)
    
    print("Procesamiento completado.")


def prepare_frames(model_cnn_path, verbose=False):
    cnn_model = load_model(model_cnn_path)
    
    model = Sequential()
    for layer in cnn_model.layers[:-1]: # go through until last layer
        model.add(layer)

    files = os.listdir(TMP_FRAMES_READY_PATH)
    ITERATIONS = math.ceil(len(files) / MAX_SEQ_LENGTH)

    frames_features = np.zeros(shape=(ITERATIONS, MAX_SEQ_LENGTH, NUM_FEATURES), dtype="float32")
    frames_mask = np.ones(shape=(ITERATIONS, MAX_SEQ_LENGTH))

    for iteration in range(0, ITERATIONS):
        idx = 0

        for i in range(0, MAX_SEQ_LENGTH):
            frame_path = TMP_FRAMES_READY_PATH + f"face_{i + (iteration * MAX_SEQ_LENGTH)}.jpg"

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
    split_video_into_frames(video_path)
    
    process_frames(TMP_FRAMES_PATH, TMP_FRAMES_READY_PATH)

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

            #TODO: We should find a better way to avoid the masked results.
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
