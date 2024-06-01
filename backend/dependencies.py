import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from keras.models import Sequential, load_model
from keras.src.saving import serialization_lib
from pydantic import BaseModel
from ipaddress import IPv4Address, IPv6Address

from routers.predict import router as predict_router
from routers.health import router as state_router
from routers.video_predictor import VideoConfig

# Needed to load models
serialization_lib.enable_unsafe_deserialization()


class AppConfig(BaseModel):
    host: IPv4Address | IPv6Address = IPv4Address("127.0.0.1")
    port: int = 8080
    cnn_path: str
    rnn_path: str
    video_config: VideoConfig


def parse_config(path: str) -> AppConfig:
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return AppConfig(**config)


def gen_init(cfg: AppConfig):
    async def initialize_models(app: FastAPI):
        print('Loading models')
        # Load CNN
        app.state.cnn_model = load_model(cfg.cnn_path)
        print('CNN loaded... OK')
        # Load feature extractor
        model_e = Sequential()
        for layer in app.state.cnn_model.layers[:-1]: # go through until last layer
            model_e.add(layer)
        app.state.feature_extractor = model_e
        print('Feature extractor loaded... OK')
        # Load RNN
        app.state.rnn_model = load_model(cfg.rnn_path)
        app.state.video_config = cfg.video_config
        print('RNN loaded... OK')
        yield
        del app.state.cnn_model
        del app.state.feature_extractor
        del app.state.rnn_model

    return asynccontextmanager(initialize_models)


def get_application(cfg: AppConfig) -> FastAPI:
    application = FastAPI(lifespan=gen_init(cfg))

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins, adjust this in production
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allows all headers
    )

    # Add routers
    application.include_router(predict_router)
    application.include_router(state_router)
    return application
