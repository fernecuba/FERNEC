import cv2
import numpy as np

from PIL import Image


def crop_image(image, bounding_box, verbose=False):
    cropped_image = image.crop((bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]))
    if verbose:
        print(cropped_image.size)
    return cropped_image


def resize_image(image, new_size, verbose=False):
    resized = image.resize(new_size, Image.LANCZOS)
    if verbose:
        print(resized.size)
    return resized


def add_padding(element, maximum_shape):
    # Get padding shapes
    padding = [(0, maximum - actual_dimension) for maximum, actual_dimension in zip(maximum_shape, element.shape)]

    return np.pad(element, padding, mode='constant', constant_values=0)


def pad_pixels(pixels):
    pixels_shapes = np.array([p.shape for p in pixels])
    unique_shapes = np.unique(pixels_shapes)

    # There is only one shape, no need to add paddings
    if len(unique_shapes) == 1:
        return pixels

    max_shape = np.amax(pixels_shapes, axis=0)
    return np.array([add_padding(p, max_shape) for p in pixels])


def get_pixels(frame, box, thumbnail_size=None, return_image=None, verbose=False):
    # frame to image
    image = Image.fromarray(frame).convert('L')

    # crop image to keep only face, if possible
    if len(box) != 0:
        image = crop_image(image, box, verbose)

    # resize image to keep new size
    if thumbnail_size:
        image = resize_image(image, thumbnail_size, verbose)

    pixels = list(image.getdata())
    if verbose:
        print(len(pixels))
    if return_image:
        return pixels, image
    return pixels


def get_frames(filename, thumbnail_size=None, verbose=False):
    img = Image.open(filename).convert('L')
    if thumbnail_size:
        img.thumbnail(thumbnail_size, Image.LANCZOS)
    if verbose:
        print(f"image name {filename} - size {img.size}")

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)