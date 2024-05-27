import os
import uvicorn
from fastapi import FastAPI
from fernec.predict import router as predict_router
from manage.get_state import router as state_router
from contextlib import asynccontextmanager
from keras.models import Sequential, load_model
from keras.src.saving import serialization_lib

# Needed to load model
serialization_lib.enable_unsafe_deserialization()

def gen_init():
    async def initialize_models(app: FastAPI):
        print('Loading models')
        model_cnn_path = os.getenv('MODEL_CNN_PATH', './fernec/ia_models/cotatest.keras')
        model_rnn_path = os.getenv('MODEL_RNN_PATH', './fernec/ia_models/cotatest_rnn_4.keras')
        # Load CNN
        app.state.cnn_model = load_model(model_cnn_path)
        print('CNN loaded... OK')
        # Load feature extractor
        model_e = Sequential()
        for layer in app.state.cnn_model.layers[:-1]: # go through until last layer
            model_e.add(layer)
        app.state.feature_extractor = model_e
        print('Feature extractor loaded... OK')
        # Load RNN
        app.state.rnn_model = load_model(model_rnn_path)
        print('RNN loaded... OK')
        yield
        del app.state.cnn_model
        del app.state.feature_extractor
        del app.state.rnn_model

    return asynccontextmanager(initialize_models)


def get_application() -> FastAPI:
    application = FastAPI(lifespan=gen_init())

    # Add routers
    application.include_router(predict_router)
    application.include_router(state_router)
    return application


# TODO: Set a logger
if __name__ == "__main__":
    app = get_application()
    print('Starting FERNEC backend')
    port = 8000
    if os.getenv("PORT"):
        port = int(os.getenv("PORT"))
    uvicorn.run(app, host='0.0.0.0', port=port)
