import cv2
import numpy as np

from PIL import Image


def open_image(file_path, shape):
    image = Image.open(file_path)
    if should_convert_to_grayscale(shape):
        image = image.convert('L')

    return np.reshape(np.array(list(image.getdata())).flatten(), shape).tolist()


def save_image(image, output_file_path):
    try:
        image.save(output_file_path)
    except Exception as e:
        print(f"exception {e} with tuple {image}")
        raise e


def should_convert_to_grayscale(shape):
    return len(shape) >= 3 and shape[2] == 1


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


def get_pixels(frame, box, channels, thumbnail_size=None, return_image=False, verbose=False):
    # frame to image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if channels == 1:
        image = image.convert('L')

    # crop image to keep only face, if possible
    if len(box) != 0:
        image = crop_image(image, box, verbose)

    # resize image to keep new size
    if thumbnail_size:
        image = resize_image(image, thumbnail_size, verbose)

    shape = thumbnail_size + (channels, )
    # pixels = list(image.getdata())
    pixels = np.reshape(np.array(list(image.getdata())).flatten(), shape).tolist()
    if verbose:
        print(len(pixels))
    if return_image:
        # print(f"about to return pixels and image: {pixels} - {image}")
        return pixels, image
    # print(f"about to return pixels: {pixels}")
    return pixels


def get_frames(filename, channels, thumbnail_size=None, verbose=False):
    img = Image.open(filename)
    if channels == 1:
        img = img.convert('L')
    if thumbnail_size:
        img.thumbnail(thumbnail_size, Image.LANCZOS)
    if verbose:
        print(f"image name {filename} - size {img.size}")

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
