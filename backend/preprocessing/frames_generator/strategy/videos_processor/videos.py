import os
import cv2
import concurrent.futures
from tqdm import tqdm
from loguru import logger
from preprocessing.frames_generator.face_detector.detector import detect_faces
from preprocessing.frames_generator.strategy.images_processor.images import get_pixels, save_image
from preprocessing.frames_generator.utils import clean_folder

def read_frame(video_path, frame_number):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    cap.release()
    return frame_number, frame if ret else None

# TODO: move me into videos_processor?
def get_frames_from_video(video_path, frames_path, batch_size, channels, thumbnail_size, frames_order_magnitude, faces_only=False):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    logger.info(f'FPS del video: {fps}')
    logger.info(f'Total frames: {total_frames}')

    num_cpus = os.cpu_count()
    raw_frames = []
    processed_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cpus) as executor:
        future_to_frame = {executor.submit(read_frame, video_path, i): i for i in range(total_frames)}

        for future in concurrent.futures.as_completed(future_to_frame):
            frame_number = future_to_frame[future]
            try:
                frame_number, frame = future.result()
                if frame is not None:
                    
                    raw_frames.append(frame)
                    if len(raw_frames) == batch_size:
                        processed_count = detect_and_save_faces(frames_path, channels, thumbnail_size, frames_order_magnitude, faces_only, raw_frames, processed_count)
                        raw_frames = []
            except Exception as exc:
                logger.error(f"Frame {frame_number} generated an exception: {exc}")


    if len(raw_frames) > 0:
        processed_count = detect_and_save_faces(frames_path, channels, thumbnail_size, frames_order_magnitude, faces_only, raw_frames, processed_count)

    logger.info(f"Processed {processed_count} frames")
    return processed_count, fps


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
