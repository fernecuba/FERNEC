import gc
import cv2
import ffmpeg
from tqdm import tqdm

from preprocessing.frames_generator.face_detector.detector import detect_faces
from preprocessing.frames_generator.strategy.images_processor.images import get_pixels, save_image
from preprocessing.frames_generator.utils import clean_folder


# TODO: move me into videos_processor?
def get_frames_from_video(video_path, frames_path, batch_size, channels, thumbnail_size, frames_order_magnitude, faces_only=False):
    
    # if video_path.endswith('.webm'):
    #     video_path = convert_video_to_mp4(video_path)

    cap = cv2.VideoCapture(video_path)
    #frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    raw_frames = []
    processed_count = 0
    success, frame = cap.read()

    while success:
        # if i % 100 == 0:
        #     gc.collect()
        # if not success:
        #     break

        raw_frames.append(frame)
        if (len(raw_frames) == batch_size):
            boxes = detect_faces(raw_frames, faces_only=faces_only)
            for j, (frame, box) in enumerate(zip(raw_frames, boxes)):
                if box is not None:
                    _, image = get_pixels(frame, box, channels, thumbnail_size, return_image=True)
                    save_image(image, frames_path +
                            f"{str(processed_count + 1).zfill(frames_order_magnitude)}.jpg")
                    processed_count += 1
            raw_frames = []

        success, frame = cap.read()

    cap.release()
    print(f"Processed {processed_count} frames")
    return processed_count

def convert_video_to_mp4(input_path):
    output_path = input_path.replace('.webm', '.mp4')
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)
    return output_path
