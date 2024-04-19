import os
import gc
import math
import time
import numpy as np
import pandas as pd

from PIL import Image
from tqdm import tqdm
from memory_profiler import profile

from preprocessing.frames_generator.utils import apply_filters_to_dataset
from preprocessing.frames_generator.database_manager.mongodb_manager import MongoDBManager
from preprocessing.frames_generator.csv_manager.csv_manager import load_into_csv
from preprocessing.frames_generator.utils import chunks_generator
from preprocessing.frames_generator.videos_processor.videos import get_frames_from_video
from preprocessing.frames_generator.utils import create_folder_if_not_exists


def process_videos(df: pd.DataFrame, config: dict):
    save_frames_from_videos(df, config)
    labels_df = create_labels_file(df, config)
    labels_df = apply_filters_to_dataset(labels_df, config["dataset_filters"])
    if config["load_into_csv"]:
        load_into_csv(labels_df, config)
    if config["database_config"]:
        upload_to_database(labels_df, config)


def save_frames_from_videos(df: pd.DataFrame, config: dict):
    """
    Saves frames from videos into config["dataset_path"] in order to
    use them later to create pixels
    """

    # TODO: define me is this necessary?
    # df.sort_values(by=config["dataset_sort"], ascending=True, inplace=True)
    videos_processed = os.listdir(config["dataset_output_path"])

    if config["verbose"]:
        print(f"Already processed {len(videos_processed)} files. {videos_processed}")

    for index, row in df.iterrows():
        if row["video_name"] in videos_processed:
            print(f"Skipping {row['video_name']} video, already generated")
            continue
        try:
            save_frames(row, config)
        except Exception as e:
            print(f"Error saving frames for {row['video_name']}: {e}")

        videos_processed.append(row["video_name"])
        if config["is_test_mode"]:
            return


def save_frames(row, config):
    if config["verbose"]:
        start_time = time.time()
        print(f"About to process {row['video_name']} video")

    folder = config["dataset_output_path"] + f"{row['video_name']}/"
    create_folder_if_not_exists(folder)
    processed_count = get_frames_from_video(
        config["dataset_path"] + row["video_file"],
        folder,
        config["batch_size"],
        config["channels"],
        config["thumbnail_size"],
        config["frames_order_magnitude"],
    )

    gc.collect()
    assert processed_count == len(os.listdir(folder))

    if config["verbose"]:
        elapsed_time = time.time() - start_time
        print(f"Processed {processed_count} frames in {(elapsed_time / 60):.2f} minutes")


# TODO: this should use "label_file" in df instead of listing dirs
def create_labels_file(labels_df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Joins frames created with its files and writes all information into one single file
    """
    if os.path.exists(config["labels_output_path"]) and os.path.isfile(config["labels_output_path"]):
        return pd.read_csv(config["labels_output_path"], sep=",", encoding="utf-8")

    # pd.options.mode.chained_assignment = None  # default='warn'
    df = pd.DataFrame()
    for index, row in labels_df.iterrows():
        video_name = row["video_name"]

        images_df = load_images(pd.DataFrame(), config["dataset_output_path"], video_name, config["dataset_sort"])
        labels_df = load_labels(f"{config['images_labels_path']}videos/{video_name}.csv")
        this_df = join_dataframes(images_df, labels_df, video_name, config["verbose"])

        if config["verbose"]:
            print(f"Video {video_name} was loaded with {len(this_df)}")
        df = pd.concat([df, this_df], ignore_index=True)

        if config["is_test_mode"]:
            break

    # pd.options.mode.chained_assignment = 'warn'
    if config["verbose"]:
        print(f"Total frames in database {len(df)}")

    print(f"sort by {config['dataset_sort']} - df columns {df.columns.values}")
    df.sort_values(by=config["dataset_sort"], ascending=True, inplace=True)
    df.to_csv(config["labels_output_path"], sep=',', encoding='utf-8', index=False)
    return df


def load_images(df, path, video_name, dataset_sort):
    df["video_name"] = video_name
    df["file_name"] = os.listdir(path + video_name)
    df["file_name"] = df["file_name"].apply(lambda x: video_name + "/" + x)
    df.sort_values(by=dataset_sort, ascending=True, inplace=True)
    return df


def load_labels(path):
    return pd.read_csv(path)


def join_dataframes(df, other_df, video_name, verbose=False):
    if len(df) != len(other_df):
        if verbose:
            print(f"Length mismatch for video {video_name}. Difference is {len(df)-len(other_df)}."
                  f" First df is {len(df)}, second df is {len(other_df)}")
        df, other_df = fix_difference_in_dataframes(df, other_df)

    for col in other_df.columns.values:
        df[col] = other_df.loc[:, col].copy()

    assert len(df) == len(other_df)
    return df


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


# TODO: use get_image in utils
def get_row_with_image(row: dict, file_path: str, shape):
    image = Image.open(file_path)
    if len(shape) >= 3 and shape[2] == 1:
        image = image.convert('L')

    row['pixels'] = np.reshape(np.array(list(image.getdata())).flatten(), shape).tolist()
    return row


@profile
def upload_to_database(df: pd.DataFrame, config: dict):
    database_config = config['database_config']
    if config["verbose"]:
        start_time = time.time()
        print(f"About to upload to uri '{database_config['uri']}',"
              f" database '{database_config['database']}' "
              f"and collection '{database_config['collection']}' "
              f"{len(df)} documents.")
    database_manager = MongoDBManager(database_config)
    database_manager.connect()
    collection = database_manager.get_collection()

    processed_documents_df = get_processed_documents(database_config)
    database_manager.delete_partial_uploads(
        collection,
        processed_documents_df["video_name"].tolist()
    )

    grouped = df.groupby("video_name")
    for group, frame in grouped:
        if group in processed_documents_df["video_name"].unique():
            if config["verbose"]:
                print(f"skipping {group}")
            continue

        if config["verbose"]:
            print(f"processing group {group} - with length {len(frame)}")

        uploaded_docs = 0
        for i, chunk_rows in enumerate(tqdm(chunks_generator(frame, config["batch_size"]),
                                       total=math.ceil(len(frame)/config["batch_size"]))):
            rows = chunk_rows.to_dict(orient='records')
            shape = config["thumbnail_size"] + (config["channels"], )
            chunk = [
                get_row_with_image(r, config["dataset_output_path"] + f"{r['video_name']}/{r['file_name']}", shape)
                for r in rows]

            result = database_manager.upload_many(collection, chunk)
            del chunk
            uploaded_docs += len(result.inserted_ids)
            if i % 5 == 0:
                gc.collect()
        assert len(frame) == uploaded_docs

        processed_documents_df = pd.concat(
            [processed_documents_df, pd.DataFrame([{"video_name": group, "uploaded_docs": uploaded_docs}])],
            ignore_index=True)
        processed_documents_df.to_csv(database_config["documents_stats_path"], sep=",", encoding="utf-8", index=False)

        if config["verbose"]:
            processed_groups_unique = processed_documents_df["video_name"].unique()
            elapsed_time = time.time() - start_time
            print(f"Processed {len(processed_groups_unique)} groups in {(elapsed_time / 60):.2f} minutes. "
                  f"Groups: {processed_groups_unique}")

    database_manager.close()


def get_processed_documents(config: dict) -> pd.DataFrame():
    if os.path.exists(config["documents_stats_path"]) and os.path.isfile(config["documents_stats_path"]):
        return pd.read_csv(config["documents_stats_path"], sep=",", encoding="utf-8")

    return pd.DataFrame(columns=["video_name", "uploaded_docs"])
