import os


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
