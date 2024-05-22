import os
import gc
import time
import pandas as pd

from preprocessing.frames_generator.strategy.base_processor import BaseProcessor
from preprocessing.frames_generator.database_manager.mongodb_manager import MongoDBManager
from preprocessing.frames_generator.strategy.videos_processor.videos import get_frames_from_video
from preprocessing.frames_generator.utils import Configurable, create_folder_if_not_exists


class VideosProcessor(BaseProcessor, Configurable):
    def __init__(self, kwargs: dict):
        super().__init__(kwargs)

    def process(self, df: pd.DataFrame):
        """
        Process videos. Saves frames and creates labels file. It may also load data into csv
        or upload to database
        """
        self.save_frames_from_videos(df)
        labels_df = self.create_labels_file(df)
        labels_df = self.apply_filters_to_dataset(labels_df, self.get("dataset_filters"))

        if self.get("load_csv"):
            self.load_into_csv(labels_df)
        if self.get("database_config"):
            self.upload_to_database(labels_df)

    def save_frames_from_videos(self, df: pd.DataFrame):
        """
        Saves frames from videos into config["dataset_path"] in order to
        """
        videos_processed = os.listdir(self.get("dataset_output_path"))

        if self.get("verbose"):
            print(f"Already processed {len(videos_processed)} files. {videos_processed}")

        for index, row in df.iterrows():
            if row["video_name"] in videos_processed:
                print(f"Skipping {row['video_name']} video, already generated")
                continue
            try:
                self.save_frames(row)
            except Exception as e:
                print(f"Error saving frames for {row['video_name']}: {e}")

            videos_processed.append(row["video_name"])
            if self.get("is_test_mode"):
                return

    def save_frames(self, row):
        start_time = time.time()
        if self.get("verbose"):
            print(f"About to process {row['video_name']} video")

        folder = self.get("dataset_output_path") + f"{row['video_name']}/"
        create_folder_if_not_exists(folder)
        processed_count = get_frames_from_video(
            self.get("dataset_path") + row["video_file"],
            folder,
            self.get("batch_size"),
            self.get("channels"),
            self.get("thumbnail_size"),
            self.get("frames_order_magnitude"),
        )

        gc.collect()
        assert processed_count == len(os.listdir(folder))

        elapsed_time = time.time() - start_time
        if self.get("verbose"):
            print(f"Processed {processed_count} frames in {(elapsed_time / 60):.2f} minutes")

    def create_labels_file(self, labels_df: pd.DataFrame) -> pd.DataFrame:
        """
        Joins frames created with its files and writes all information into one single file
        """
        if os.path.exists(self.get("labels_output_path")) and os.path.isfile(self.get("labels_output_path")):
            return pd.read_csv(self.get("labels_output_path"), sep=",", encoding="utf-8")

        pd.options.mode.chained_assignment = None  # default='warn'
        df = pd.DataFrame()
        for index, row in labels_df.iterrows():
            video_name = row["video_name"]

            images_df = self.load_images(pd.DataFrame(), self.get("dataset_output_path"), video_name,
                                         self.get("dataset_sort"))
            labels_df = self.load_labels(f"{self.get('images_labels_path')}videos/{video_name}.csv")
            this_df = self.join_dataframes(images_df, labels_df, video_name)

            if self.get("verbose"):
                print(f"Video {video_name} was loaded with {len(this_df)}")
            df = pd.concat([df, this_df], ignore_index=True)

            if self.get("is_test_mode"):
                break

        pd.options.mode.chained_assignment = 'warn'
        if self.get("verbose"):
            print(f"Total frames in database {len(df)}")

        print(f"sort by {self.get('dataset_sort')} - df columns {df.columns.values}")
        df.sort_values(by=self.get("dataset_sort"), ascending=True, inplace=True)
        df.to_csv(self.get("labels_output_path"), sep=',', encoding='utf-8', index=False)
        return df

    @staticmethod
    def load_images(df, path, video_name, dataset_sort):
        df["video_name"] = video_name
        df["file_name"] = os.listdir(path + video_name)
        df["file_name"] = df["file_name"].apply(lambda x: video_name + "/" + x)
        df.sort_values(by=dataset_sort, ascending=True, inplace=True)
        return df

    @staticmethod
    def load_labels(path):
        return pd.read_csv(path)

    def join_dataframes(self, df, other_df, video_name):
        if len(df) != len(other_df):
            if self.get("verbose"):
                print(f"Length mismatch for video {video_name}. Difference is {len(df) - len(other_df)}."
                      f" First df is {len(df)}, second df is {len(other_df)}")
            df, other_df = self.fix_difference_in_dataframes(df, other_df)

        for col in other_df.columns.values:
            df[col] = other_df.loc[:, col].copy()

        assert len(df) == len(other_df)
        return df

    @staticmethod
    def fix_difference_in_dataframes(df, other_df):
        if len(df) == len(other_df):
            return df, other_df

        if len(df) < len(other_df):
            repeat_samples = len(other_df) - len(df)
            df = pd.concat([df, df.tail(repeat_samples)], ignore_index=True)
        else:
            repeat_samples = len(df) - len(other_df)
            other_df = pd.concat([other_df, other_df.tail(repeat_samples)], ignore_index=True)

        assert len(df) == len(other_df)

        return df, other_df

    def upload_to_database(self, df: pd.DataFrame):
        database_config = self.get('database_config')
        start_time = time.time()
        if self.get("verbose"):
            print(f"About to upload to uri '{database_config['uri']}',"
                  f" database '{database_config['database']}' "
                  f"and collection '{database_config['collection']}' "
                  f"{len(df)} documents.")
        database_manager = MongoDBManager(database_config)
        database_manager.connect()
        collection = database_manager.get_collection()

        processed_documents_df = self.get_processed_documents(database_config)
        database_manager.delete_partial_uploads(
            collection,
            processed_documents_df["video_name"].tolist()
        )

        grouped = df.groupby("video_name")
        for group, frame in grouped:
            if group in processed_documents_df["video_name"].unique():
                if self.get("verbose"):
                    print(f"skipping {group}")
                continue

            if self.get("verbose"):
                print(f"processing group {group} - with length {len(frame)}")

            uploaded_docs = self.upload_docs(frame, collection, database_manager)

            processed_documents_df = pd.concat(
                [processed_documents_df, pd.DataFrame([{"video_name": group, "uploaded_docs": uploaded_docs}])],
                ignore_index=True)
            processed_documents_df.to_csv(database_config["documents_stats_path"], sep=",",
                                          encoding="utf-8", index=False)

            if self.get("verbose"):
                processed_groups_unique = processed_documents_df["video_name"].unique()
                elapsed_time = time.time() - start_time
                print(f"Processed {len(processed_groups_unique)} groups in {(elapsed_time / 60):.2f} minutes. "
                      f"Groups: {processed_groups_unique}")

        database_manager.close()

    @staticmethod
    def get_processed_documents(config: dict) -> pd.DataFrame():
        if os.path.exists(config["documents_stats_path"]) and os.path.isfile(config["documents_stats_path"]):
            return pd.read_csv(config["documents_stats_path"], sep=",", encoding="utf-8")

        return pd.DataFrame(columns=["video_name", "uploaded_docs"])
