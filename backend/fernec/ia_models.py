import os

from tensorflow.keras.models import load_model, Sequential
from keras.src.saving import serialization_lib


def get_cnn_model(path):
    original_cnn_model = load_model(path)
    print(f"Loaded CNN model from path {path}")
    sequential_model = Sequential()
    for layer in original_cnn_model.layers[:-1]:  # go through until last layer
        sequential_model.add(layer)
    return sequential_model


def get_rnn_model(path):
    original_rnn_model = load_model(model_rnn_path)
    print(f"Loaded RNN model from path {path}")
    return original_rnn_model


# Needed to load model
serialization_lib.enable_unsafe_deserialization()
# Load model
model_cnn_path = os.getenv('MODEL_CNN_PATH', './fernec/ia_models/cotatest.keras')
model_rnn_path = os.getenv('MODEL_RNN_PATH', './fernec/ia_models/cotatest_rnn_4.keras')
cnn_model = get_cnn_model(model_cnn_path)
rnn_model = get_rnn_model(model_rnn_path)
