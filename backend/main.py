import os
import uvicorn
from loguru import logger
from dependencies import parse_config, get_application

def create_app():
    config_path = os.getenv("CONFIG_FILE") if os.getenv("CONFIG_FILE") else "./config.yaml"
    logger.info(f"Use config file: {config_path}")
    cfg = parse_config(config_path)
    app = get_application(cfg)
    return app, cfg

if __name__ == "__main__":
    app, cfg = create_app()
    if app is None:
        raise TypeError("app not instantiated")
    logger.info('Starting FERNEC backend')
    uvicorn.run(app, host=str(cfg.host), port=cfg.port)
