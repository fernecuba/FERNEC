import os
import shutil
import time
import numpy as np
import pandas as pd

from preprocessing.frames_generator.images_processor.images import get_frames, pad_pixels, get_pixels
from preprocessing.frames_generator.face_detector.detector import detect_faces
from preprocessing.frames_generator.utils import apply_filters_to_dataset


def process_images(df: pd.DataFrame, config: dict):
    """
    Process images. It may generate one csv containing pixels and labels
    and it may also rearrange files properly to use tensorflow's image_dataset_from_directory
    """
    df.sort_values(by=config["dataset_sort"], ascending=True, inplace=True)
    df = apply_filters_to_dataset(df, config["dataset_filters"])
    # TODO: load_into_csv should be a separate handler. such as csv_manager or whatever
    if config["load_into_csv"]:
        load_into_csv(df, config)
    if config["rearrange_files"]:
        rearrange_files(df, config)


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
        lambda r: get_frames(config["dataset_path"] + r["file_name"],
                             config["channels"]), axis=1)

    # pad pixels when necessary
    pixels_padded = pad_pixels(df_split["frame"].tolist())
    df_split["boxes"] = detect_faces(pixels_padded)

    df_split["pixels"] = df_split.apply(
        lambda row: get_pixels(row["frame"], row["boxes"], config["channels"],
                               config["thumbnail_size"], return_image=None), axis=1)

    df_split.drop(columns=["boxes", "frame"], inplace=True)
    set_header = (i == 0)
    df_split.to_csv(config["output_path"] + config["temp_path"] + f"{config['dataset']}_{i}.csv",
                    sep=',', encoding='utf-8', headers=set_header, index=False)

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


def rearrange_files(df: pd.DataFrame, config: dict):
    if config["verbose"]:
        start_process = time.time()

    source_folder = config["dataset_path"]
    destination_folder = config["destination_folder"]
    failures = df.apply(lambda r: move_file(r["file_name"], r["labels_expression"], source_folder, destination_folder),
                        axis=1)
    failed_files = [file_name for file_name in failures.unique() if file_name is not None]

    if config["verbose"]:
        elapsed_time = time.time() - start_process
        print(f"Processed {len(df)} in {(elapsed_time / 60):.2f} minutes. Failed {len(failed_files)} files."
              f"They are: {failed_files}")


def move_file(file_name, labels_name, source_folder, destination_folder):
    try:
        shutil.move(
            source_folder + file_name,
            destination_folder + f"{labels_name}/{file_name}"
        )
    except Exception as e:
        return file_name
