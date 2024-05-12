import os
import cv2
import pandas as pd
import numpy as np
from facenet_pytorch import MTCNN as facenet_MTCNN
from PIL import Image
from keras.models import load_model

# Temp path to save the frames extracted from the video
TMP_FRAMES_PATH = "./temp/frames/"
# In this path we will save the frames that are ready to be predicted
TMP_FRAMES_READY_PATH = "temp/frames_ready/"

HEIGHT = 48
WIDTH = 48
CHANNELS = 1
HEIGHT_POSITION = 2
WIDTH_POSITION = 3
Y = 0
X = 1

def clean_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("La ruta especificada no es una carpeta.")

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)

def split_video_into_frames(video_path, target_fps=29):
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

# This function was used for the old face detector
def get_points(box):
    '''
        Args:
            box (tuple): consisting of (x, y, w, h) were w is width and h is height
        Returns:
            tuple: (x, y, x + w, y + h) which can be thought as (x1, y1, x2, y2)
    '''
    # return [box[Y], box[X], box[Y] + box[HEIGHT], box[X] + box[WIDTH]]
    # return box.tolist()
    return box


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
    image = Image.fromarray(frame).convert('L')

    if box is not None:
        # get boxes
        if len(box) != 0:
            if verbose:
                print(f"There is a box to crop: {box}")
            # Crop image to keep only the face
            cropped_image = crop_image(image, box, verbose)
            # Resize the cropped image to 48x48
            resized_image = cropped_image.resize((48, 48))
            # Save the resized image to the output folder
            output_path = os.path.join(output_folder, f"face_{len(os.listdir(output_folder))}.jpg")
            resized_image.save(output_path)
            if verbose:
                print(f"Saved image to {output_path}")
        else:
            print("No box detected for cropping")

def process_frames(frames_path, frames_ready_path, batch_size=20):
    detector = facenet_MTCNN()

    if not os.path.exists(frames_ready_path):
        os.makedirs(frames_ready_path)

    clean_folder(frames_ready_path)
    
    image_files = [f for f in os.listdir(frames_path) if f.endswith(('.jpg', '.png'))]

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

def get_pixels(filename, thumbnail_size=None, verbose=False):
    if verbose:
        print(f"image name {filename}")

    img = Image.open(filename) #.convert('L')
    if thumbnail_size:
        img.thumbnail(thumbnail_size, Image.LANCZOS)
    if verbose:
        print(img.size)
        display.display(img)

    return list(img.getdata())

def get_label_processor(labels_series):
    label_processor = keras.layers.StringLookup(
      num_oov_indices=0, vocabulary=np.unique(labels_series)
    )
    print(label_processor.get_vocabulary())
    return label_processor


def prepare_data(data, height, width, channels):
    """ Prepare data for modeling
        input: data frame with labels und pixel data
        output: image and label array """

    image_array = np.zeros(shape=(len(data), height, width, channels))

    data_image = data["pixels"].apply(lambda x: np.reshape(np.array(x).flatten(), (height, width, channels)))

    # TODO: if data_image.values returns values in order, this can be replaced with np.array(data_image.values)
    for i, pixel in enumerate(data_image):
        image_array[i] = pixel

    return image_array

def get_frames_to_predict(frames_ready_path):
    
    files = os.listdir(frames_ready_path)
    df = pd.DataFrame({
        "file_name": files
    })

    pixels_list = []
    for index, row in df.iterrows():
        pixels_list.append(get_pixels(frames_ready_path + f"{row['file_name']}"))
    
    # Asignamos la lista de píxeles a la columna 'pixels'
    df["pixels"] = pixels_list    
    
    image_array = prepare_data(df, HEIGHT, WIDTH, CHANNELS)
    images = image_array.reshape((image_array.shape[0], HEIGHT, WIDTH, CHANNELS))
    images = images.astype('float32')/255

    return images

def predict_video(video_path, model_path):
    split_video_into_frames(video_path)
    
    process_frames(TMP_FRAMES_PATH, TMP_FRAMES_READY_PATH)
    
    frames_to_predict = get_frames_to_predict(TMP_FRAMES_READY_PATH)

    model_imported = load_model(model_path)

    print("Loaded model from path " + model_path)

    prediction = model_imported.predict(frames_to_predict)

    return prediction

def print_prediction(prediction):
    class_vocab = [
    "Neutral", "Anger", "Disgust", "Fear", "Happiness", "Sadness", "Surprise", "Other"
    ]
    print(class_vocab)
    results = []
    for i, result in enumerate(prediction):
        result_argmax = result.argmax()
        result_label = class_vocab[result_argmax]
    
        results.append(f"frame {i} - result {result_label}")
    
    return results