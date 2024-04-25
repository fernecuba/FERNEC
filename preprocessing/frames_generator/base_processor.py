import os
import gc
import time
import math
import numpy as np
import pandas as pd

from tqdm import tqdm

from preprocessing.frames_generator.images_processor.images import open_image
from preprocessing.frames_generator.utils import Configurable, chunks_generator


class BaseProcessor(Configurable):
    def __init__(self, kwargs: dict):
        super().__init__(kwargs)

    def upload_docs(self, iterable, collection, database_manager):
        """
        Uploads an iterable to MongoDB and returns number of documents uploaded
        """
        uploaded_docs = 0
        for i, chunk_rows in enumerate(tqdm(chunks_generator(iterable, self.get("batch_size")),
                                            total=math.ceil(len(iterable) / self.get("batch_size")))):
            rows = chunk_rows.to_dict(orient='records')
            shape = self.get("thumbnail_size") + (self.get("channels"),)
            chunk = [
                self.get_row_with_image(r, self.get("dataset_output_path") + f"{r['video_name']}/{r['file_name']}",
                                        shape)
                for r in rows]

            result = database_manager.upload_many(collection, chunk)
            del chunk
            uploaded_docs += len(result.inserted_ids)
            if i % 5 == 0:
                gc.collect()
        assert len(iterable) == uploaded_docs
        return uploaded_docs

    @staticmethod
    def get_row_with_image(row: dict, file_path: str, shape):
        row['pixels'] = open_image(file_path, shape)
        return row

    def load_into_csv(self, df: pd.DataFrame):
        """
        Saves a dataframe into csv
        """
        start_process = time.time()
        files_processed = [file for file in os.listdir(self.get("output_path") + self.get("temp_path"))
                           if ".csv" in file and "~lock." not in file]
        if self.get("verbose"):
            print(f"Already processed {len(files_processed)} files. {files_processed}")

        # TODO: test me. Can i use chunks_generator here? Can I use self.get("batch_size")?
        # df_splitted = chunks_generator(df, self.get("array_split"))
        df_splitted = np.array_split(df, self.get("array_split"))
        for i, df_split in enumerate(df_splitted):
            if i < len(files_processed):
                continue
            self.save_dataframe(df_split.copy(), i, )

            if self.get("is_test_mode"):
                break

        processed = self.join_results()

        elapsed_time = time.time() - start_process
        print(f"Processed {processed} in {(elapsed_time / 60):.2f} minutes")

    def save_dataframe(self, df_split: pd.DataFrame, i: int):
        start = time.time()
        if self.get("verbose"):
            print(f"About to process {i} dataset {len(df_split)} long")

        shape = self.get("thumbnail_size") + (self.get("channels"),)
        frames = df_split.apply(
            lambda r: open_image(self.get("dataset_output_path") + r["file_name"],
                                 shape), axis=1)
        df_split["frame"] = frames

        set_header = (i == 0)
        df_split.to_csv(self.get("output_path") + self.get("temp_path") + f"{self.get('dataset')}_{i}.csv",
                        sep=',', encoding='utf-8', header=set_header, index=False)

        elapsed_time = time.time() - start
        if self.get("verbose"):
            print(f"Processed {len(df_split)} in {(elapsed_time / 60):.2f} minutes")
        del df_split
        del frames
        gc.collect()

    def join_results(self) -> int:
        output_file_path = self.get("output_path") + f"{self.get('dataset')}.csv"
        if os.path.exists(output_file_path) and os.path.isfile(output_file_path):
            return 0

        counter = 0
        for i in range(self.get("array_split")):
            if self.get("verbose"):
                print(f"About to write file {i} - lines already written {counter}")
            with open(self.get("output_path") + self.get("temp_path") + f"{self.get('dataset')}_{i}.csv",
                      "rt") as read_file:
                with open(output_file_path, "a") as write_file:
                    for line in read_file:
                        write_file.write(line)
                        counter += 1
            gc.collect()

        return counter
