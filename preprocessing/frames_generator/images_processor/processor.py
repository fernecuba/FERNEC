import os
import time
import numpy as np
import pandas as pd

from preprocessing.frames_generator.images_processor.images import get_frames, pad_pixels, get_pixels
from preprocessing.frames_generator.face_detector.detector import detect_faces


def process_images(df: pd.DataFrame, config: dict):
    """
    Process images and generates one csv containing pixels and labels
    """

    start_process = time.time()
    df.sort_values(by=config["dataset_sort"], ascending=True, inplace=True)
    df = apply_filters_to_dataset(df, config["dataset_filters"])
    # TODO: is this unnecessary?
    files_processed = [file for file in os.listdir(config["output_path"] + config["temp_path"])
                       if ".csv" in file and "~lock." not in file]
    if config["verbose"]:
        print(f"Already processed {len(files_processed)} files. {files_processed}")

    df_splitted = np.array_split(df, config["array_split"])
    for i, df_split in enumerate(df_splitted):
        if i < len(files_processed):
            continue
        process_dataframe(df_split, i, config)

        if config["is_test_mode"]:
            break

    processed = join_results(config)

    elapsed_time = time.time() - start_process
    print(f"Processed {processed} in {(elapsed_time / 60):.2f} minutes")


def process_dataframe(df_split: pd.DataFrame, i: int, config: dict):
    if config["verbose"]:
        start = time.time()
        print(f"About to process {i} dataset {len(df_split)} long")

    df_split["frame"] = df_split.apply(
        lambda r: get_frames(config["dataset_path"] + f'{r["video_name"]}/{r["file_name"]}'), axis=1)

    # pad pixels when necessary
    pixels_padded = pad_pixels(df_split["frame"].tolist())
    df_split["boxes"] = detect_faces(pixels_padded)

    df_split["pixels"] = df_split.apply(
        lambda row: get_pixels(row["frame"], row["boxes"], config["thumbnail_size"], return_image=None), axis=1)

    df_split.drop(columns=["boxes", "frame"], inplace=True)
    set_header = (i == 0)
    df_split.to_csv(config["output_path"] + config["temp_path"] + f"{config['dataset']}_{i}.csv",
                    sep=',', encoding='utf-8', header=set_header, index=False)

    if config["verbose"]:
        elapsed_time = time.time() - start
        print(f"Processed {len(df_split)} in {(elapsed_time / 60):.2f} minutes")


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


def apply_filters_to_dataset(df: pd.DataFrame, filters: dict):
    for column, valid_values in filters.items():
        df = df.loc[df[column].isin(valid_values)]
    return df
