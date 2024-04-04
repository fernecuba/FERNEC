# TODO: please god rename me
import os
import cv2
from PIL import Image


def create_folder_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_image_into_file(image, output_file_path):
    # print(pixels)
    image.save(output_file_path)
    # cv2.imwrite(output_file_path, pixels)
