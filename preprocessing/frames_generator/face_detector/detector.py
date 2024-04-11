import torch
from facenet_pytorch import MTCNN

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))


detector = MTCNN(selection_method="largest", min_face_size=40)


def detect_faces(pixels):
    detection = detector.detect(pixels)[0]
    boxes = []
    for face in detection:
        if face is not None and len(face) != 0:
            # detected is a tuple, and we want to keep the first position containing
            # the bounding boxes
            boxes.append(face[0])
        else:
            boxes.append([])
    return boxes
