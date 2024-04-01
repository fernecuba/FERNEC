import os
import gc
import time
import pandas as pd

from utils import create_folder_if_not_exists
from videos_processor.videos import get_frames_from_video


def process_videos(df: pd.DataFrame, config: dict):
    save_frames_from_videos(df, config)
    create_labels_file(config)


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
        config["frames_batch_size"],
        config["thumbnail_size"],
        config["frames_order_magnitude"],
    )

    gc.collect()
    assert processed_count == len(os.listdir(folder))

    if config["verbose"]:
        elapsed_time = time.time() - start_time
        print(f"Processed {processed_count} frames in {(elapsed_time / 60):.2f} minutes")


# TODO: this should use "label_file" in df instead of listing dirs
def create_labels_file(config):
    # pd.options.mode.chained_assignment = None  # default='warn'
    df = pd.DataFrame()

    for video_name in os.listdir(config["dataset_output_path"]):
        images_df = load_images(pd.DataFrame(), config["dataset_output_path"], video_name, config["dataset_sort"])
        labels_df = load_labels(f"{config['images_labels_path']}videos/{video_name}.csv")
        this_df = join_dataframes(images_df, labels_df, video_name, config["verbose"])

        if config["verbose"]:
            print(f"Video {video_name} was loaded with {len(this_df)}")
        df = pd.concat([df, this_df], ignore_index=True)

    # pd.options.mode.chained_assignment = 'warn'
    if config["verbose"]:
        print(f"Total frames in database {len(df)}")

    print(f"sort by {config['dataset_sort']} - df columns {df.columns.values}")
    df.sort_values(by=config["dataset_sort"], ascending=True, inplace=True)
    df.to_csv(config["labels_output_path"], sep=',', encoding='utf-8', index=False)


def load_images(df, path, video_name, dataset_sort):
    df["file_name"] = os.listdir(path + video_name)
    df["video_name"] = video_name
    df.sort_values(by=dataset_sort, ascending=True, inplace=True)
    return df


def load_labels(path):
    return pd.read_csv(path)


def join_dataframes(df, other_df, video_name, verbose=False):
    if len(df) != len(other_df):
        if verbose:
            print(f"Length mismatch for video {video_name}. Difference is {len(df)-len(other_df)}. First df is {len(df)},"
                  f" second df is {len(other_df)}")
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
