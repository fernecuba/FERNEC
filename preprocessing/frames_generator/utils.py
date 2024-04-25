import os
import pandas as pd


class Configurable:
    def __init__(self, config: dict):
        for key in config:
            setattr(self, key, config[key])

    def get(self, attribute):
        return self.__getattribute__(attribute)


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_image_into_file(image, output_file_path):
    image.save(output_file_path)


def chunks_generator(complete_list, size):
    """Divide a list into chunks of specified size."""
    for i in range(0, len(complete_list), size):
        yield complete_list[i:i + size]


def apply_filters_to_dataset(df: pd.DataFrame, filters: dict):
    for column, valid_values in filters.items():
        df = df.loc[df[column].isin(valid_values)]
    return df
