import pandas as pd

from videos_processor.processor import VideosProcessor
from images_processor.processor import ImagesProcessor


def run(config):
    processor = get_strategy(config)

    df = pd.read_csv(config["labels_path"], sep=",", encoding="utf-8")
    if config["verbose"]:
        print(f"Strategy {config['source']}: about to process {df.shape} dataframe")
    processor.process(df)


def get_strategy(config):
    if config["source"] == "images":
        return ImagesProcessor(config)
    elif config["source"] == "videos":
        return VideosProcessor(config)
    else:
        raise NotImplementedError(f"Source {config['source']} not implemented")
