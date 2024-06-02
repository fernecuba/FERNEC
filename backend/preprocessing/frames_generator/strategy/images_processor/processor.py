import os
import time

import shutil
import numpy as np
import pandas as pd
from loguru import logger
from preprocessing.frames_generator.strategy.base_processor import BaseProcessor
from preprocessing.frames_generator.strategy.images_processor.images import get_frames, pad_pixels, get_pixels, save_image
from preprocessing.frames_generator.face_detector.detector import detect_faces
from preprocessing.frames_generator.utils import Configurable, create_folder_if_not_exists


class ImagesProcessor(BaseProcessor, Configurable):
    def __init__(self, kwargs: dict):
        super().__init__(kwargs)

    def process(self, df: pd.DataFrame):
        """
        Process images. Saves processed frames and creates labels file. It may also load data into csv
        or rearrange files properly to use tensorflow's image_dataset_from_directory
        """
        df.sort_values(by=self.get("dataset_sort"), ascending=True, inplace=True)
        df = self.apply_filters_to_dataset(df, self.get("dataset_filters"))
        self.process_images(df)
        if self.get("load_csv"):
            self.load_into_csv(df)
        if self.get("rearrange_by_labels"):
            logger.info(df.info())
            self.rearrange_files(df)

    def process_images(self, df):
        processed_images_df = self.get_processed_images()

        df_splitted = np.array_split(df, self.get("array_split"))
        for i, df_split in enumerate(df_splitted):
            if i < len(processed_images_df):
                continue
            start = time.time()

            logger.debug(f"About to process {i} dataset {len(df_split)} long")

            self.save_frames(df_split.copy())

            processed_images_df = pd.concat(
                [processed_images_df, pd.DataFrame([{"splitted": i, "processed_images": len(df_split)}])],
                ignore_index=True)
            processed_images_df.to_csv(self.get("processed_stats_path"), sep=",",
                                       encoding="utf-8", index=False)

            elapsed_time = time.time() - start
            
            logger.debug(f"Processed {len(df_split)} in {(elapsed_time / 60):.2f} minutes")

            if self.get("is_test_mode"):
                break

    def save_frames(self, df: pd.DataFrame):
        df["frame"] = df.apply(
            lambda r: get_frames(self.get("dataset_path") + r["file_name"],
                                 self.get("channels")), axis=1)

        # pad pixels when necessary
        pixels_padded = pad_pixels(df["frame"].tolist())
        df["boxes"] = detect_faces(pixels_padded)

        df["pixels"], df["image"] = zip(*df.apply(
            lambda row: get_pixels(row["frame"], row["boxes"], self.get("channels"),
                                   self.get("thumbnail_size"), return_image=True), axis=1))

        df.apply(lambda r: save_image(r["image"], f"{self.get('dataset_output_path')}/{r['file_name']}"), axis=1)

    def rearrange_files(self, df):
        start = time.time()
        
        logger.debug(f"About to process dataset {len(df)} long")

        source_folder = self.get("dataset_output_path")
        destination_folder = self.get("destination_folder")
        logger.info(f"source_folder is {source_folder}, destination_folder is {destination_folder}")
        failures = df.apply(
            lambda r: self.move_file(r["file_name"], r["labels_expression"],
                                     source_folder, destination_folder), axis=1)
        failed_files = [file_name for file_name in failures.unique() if file_name is not None]

        elapsed_time = time.time() - start
        
        logger.debug(f"Processed {len(df)} in {(elapsed_time / 60):.2f} minutes. Failed {len(failed_files)} files.")

    @staticmethod
    def move_file(file_name, labels_name, source_folder, destination_folder):
        create_folder_if_not_exists(destination_folder + labels_name)
        try:
            shutil.move(
                source_folder + file_name,
                destination_folder + f"{labels_name}/{file_name}"
            )
        except Exception as e:
            logger.exception(f"move_file failed")
            return file_name

    def get_processed_images(self) -> pd.DataFrame():
        if os.path.exists(self.get("processed_stats_path")) and os.path.isfile(self.get("processed_stats_path")):
            return pd.read_csv(self.get("processed_stats_path"), sep=",", encoding="utf-8")

        return pd.DataFrame(columns=["splitted", "processed_images"])
