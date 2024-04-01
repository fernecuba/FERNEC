import os
import time
import numpy as np
import pandas as pd

from images_processor.images import get_frames, pad_pixels, get_pixels
from face_detector.detector import detect_faces


def process_images(df: pd.DataFrame, config: dict):
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

    results_df = join_results(config)

    elapsed_time = time.time() - start_process
    print(f"Processed {len(results_df)} in {(elapsed_time / 60):.2f} minutes")


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
    df_split.to_csv(config["output_path"] + config["temp_path"] + f"{config['dataset']}_{i}.csv", sep=',',
                    encoding='utf-8', index=False)

    if config["verbose"]:
        elapsed_time = time.time() - start
        print(f"Processed {len(df_split)} in {(elapsed_time / 60):.2f} minutes")


def join_results(config: dict) -> pd.DataFrame:
    files_processed = [file for file in os.listdir(config["output_path"] + "/temp") if ".csv" in file]
    results_df = pd.DataFrame()
    for file_name in files_processed:
        processed_df = pd.read_csv(config["output_path"] + config["temp_path"] + file_name,
                                   sep=',', encoding='utf-8')
        processed_df["pixels"] = processed_df["pixels"].apply(eval)
        results_df = pd.concat([results_df, processed_df])

    results_df.to_csv(config["output_path"] + f"{config['dataset']}.csv", sep=',',
                      encoding='utf-8', index=False)
    return results_df


def apply_filters_to_dataset(df: pd.DataFrame, filters: dict):
    for column, valid_values in filters.items():
        df = df.loc[df[column].isin(valid_values)]
    return df
