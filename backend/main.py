import os
import uvicorn

from dependencies import parse_config, get_application


# TODO: Set a logger
if __name__ == "__main__":
    config_path = os.getenv("CONFIG_FILE") if os.getenv("CONFIG_FILE") else "./config.yaml"
    print(f"Use config file: {config_path}")
    cfg = parse_config(config_path)
    app = get_application(cfg)
    if app is None:
        raise TypeError("app not instantiated")
    print('Starting FERNEC backend')
    uvicorn.run(app, host=str(cfg.host), port=cfg.port)
