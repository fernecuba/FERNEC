import pandas as pd
from images_processor.processor import process_images
from videos_processor.processor import process_videos


def run_strategy(config):
    df = pd.read_csv(config["labels_path"], sep=",", encoding="utf-8")

    if config["source"] == "images":
        if config["verbose"]:
            print(f"About to process {df.shape} dataframe")
        process_images(df, config)

    elif config["source"] == "videos":
        if config["verbose"]:
            print(f"About to process {df.shape} dataframe")
        process_videos(df, config)

    else:
        raise NotImplementedError(f"Source {config['source']} not implemented")
