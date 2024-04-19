import os
import gc
import time
import numpy as np
import pandas as pd
from preprocessing.frames_generator.images_processor.images import open_image
from memory_profiler import profile


def load_into_csv(df: pd.DataFrame, config: dict):
    start_process = time.time()
    files_processed = [file for file in os.listdir(config["output_path"] + config["temp_path"])
                       if ".csv" in file and "~lock." not in file]
    if config["verbose"]:
        print(f"Already processed {len(files_processed)} files. {files_processed}")

    df_splitted = np.array_split(df, config["array_split"])
    for i, df_split in enumerate(df_splitted):
        if i < len(files_processed):
            continue
        save_dataframe(df_split.copy(), i, config)

        if config["is_test_mode"]:
            break

    processed = join_results(config)

    elapsed_time = time.time() - start_process
    print(f"Processed {processed} in {(elapsed_time / 60):.2f} minutes")


def save_dataframe(df_split: pd.DataFrame, i: int, config: dict):
    if config["verbose"]:
        start = time.time()
        print(f"About to process {i} dataset {len(df_split)} long")

    shape = config["thumbnail_size"] + (config["channels"],)
    frames = df_split.apply(
        lambda r: open_image(config["dataset_output_path"] + r["file_name"],
                             shape), axis=1)
    df_split["frame"] = frames

    set_header = (i == 0)
    df_split.to_csv(config["output_path"] + config["temp_path"] + f"{config['dataset']}_{i}.csv",
                    sep=',', encoding='utf-8', header=set_header, index=False)

    if config["verbose"]:
        elapsed_time = time.time() - start
        print(f"Processed {len(df_split)} in {(elapsed_time / 60):.2f} minutes")
    del df_split
    del frames
    gc.collect()

def join_results(config: dict) -> int:
    output_file_path = config["output_path"] + f"{config['dataset']}.csv"
    if os.path.exists(output_file_path) and os.path.isfile(output_file_path):
        with open(output_file_path, "r") as file:
            return len(file.readlines())

    with open(output_file_path, "a") as write_file:
        for i in range(config["array_split"]):
            with open(config["output_path"] + config["temp_path"] + f"{config['dataset']}_{i}.csv", "rt") as read_file:
                for line in read_file:
                    write_file.write(line)

    with open(output_file_path, "r") as file:
        return len(file.readlines())
