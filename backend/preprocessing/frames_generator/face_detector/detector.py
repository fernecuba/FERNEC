import torch
from facenet_pytorch import MTCNN
from loguru import logger

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
logger.info('Running on device: {}'.format(device))


detector = MTCNN(selection_method="largest", min_face_size=40)


def detect_faces(pixels, faces_only=False):
    detection = detector.detect(pixels)[0]
    boxes = []
    for face in detection:
        if face is not None and len(face) != 0:
            # detected is a tuple, and we want to keep the first position containing
            # the bounding boxes
            boxes.append(face[0])
        else:
            if faces_only:
                boxes.append(face)
            else:
                boxes.append([])
    return boxes
