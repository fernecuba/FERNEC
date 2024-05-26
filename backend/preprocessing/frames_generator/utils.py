import os
import shutil

class Configurable:
    def __init__(self, config: dict):
        for key in config:
            setattr(self, key, config[key])

    def get(self, attribute):
        return self.__getattribute__(attribute)


# this method could be moved to BaseProcessor
def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def chunks_generator(complete_list, size):
    """Divide a list into chunks of specified size."""
    for i in range(0, len(complete_list), size):
        yield complete_list[i:i + size]

def clean_folder(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("Specified path is not a folder")

    for file in os.listdir(folder_path):
        full_path = os.path.join(folder_path, file)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
