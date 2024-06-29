import gc
import cv2
import ffmpeg
from tqdm import tqdm
from loguru import logger
from preprocessing.frames_generator.face_detector.detector import detect_faces
from preprocessing.frames_generator.strategy.images_processor.images import get_pixels, save_image
from preprocessing.frames_generator.utils import clean_folder


# TODO: move me into videos_processor?
def get_frames_from_video(video_path, frames_path, batch_size, channels, thumbnail_size, frames_order_magnitude, faces_only=False):
    cap = cv2.VideoCapture(video_path)
    raw_frames = []
    processed_count = 0
    success, frame = cap.read()
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count // fps)
    logger.info(f'FPS del video: {fps}')

    while success:
        raw_frames.append(frame)
        if len(raw_frames) == batch_size:
            processed_count = detect_and_save_faces(frames_path, channels, thumbnail_size, frames_order_magnitude, faces_only, raw_frames, processed_count)
            raw_frames = []
        success, frame = cap.read()

    cap.release()

    if len(raw_frames) > 0:
        processed_count = detect_and_save_faces(frames_path, channels, thumbnail_size, frames_order_magnitude, faces_only, raw_frames, processed_count)

    logger.info(f"Processed {processed_count} frames")
    return processed_count, fps, duration


def detect_and_save_faces(frames_path, channels, thumbnail_size, frames_order_magnitude, faces_only, raw_frames, processed_count):
    boxes = detect_faces(raw_frames, faces_only=faces_only)
    for j, (frame, box) in enumerate(zip(raw_frames, boxes)):
        if box is not None:
            _, image = get_pixels(frame, box, channels, thumbnail_size, return_image=True)
            save_image(image, frames_path +
                       f"{str(processed_count + 1).zfill(frames_order_magnitude)}.jpg")
            processed_count += 1

    return processed_count


def frames_to_seconds(frames, fps):
    return int(frames // fps)
