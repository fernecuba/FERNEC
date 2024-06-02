import os
import sys
import uvicorn
from loguru import logger
from dependencies import parse_config, get_application

if __name__ == "__main__":
    config_path = os.getenv("CONFIG_FILE") if os.getenv("CONFIG_FILE") else "./config.yaml"
    cfg = parse_config(config_path)
    logger.info(f"Use config file: {config_path}")
    logger.remove()
    logger.add(sys.stderr, level=cfg.log_level)
    app = get_application(cfg)
    if app is None:
        raise TypeError("app not instantiated")
    logger.info('Starting FERNEC backend')
    uvicorn.run(app, host=str(cfg.host), port=cfg.port)