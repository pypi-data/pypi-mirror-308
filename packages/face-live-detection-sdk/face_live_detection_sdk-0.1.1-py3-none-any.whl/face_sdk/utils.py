# utils.py

import base64
import cv2
import numpy as np

def decode_base64_image(image_base64):
    image_data = base64.b64decode(image_base64)
    return cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
