import cv2
import numpy as np
import easyocr
from PIL import Image
from io import BytesIO

reader = easyocr.Reader(['ko', 'en'], gpu=False)

def detect_plate_number(img_np: np.ndarray) -> str:
    processed = preprocess_image(img_np)

    result = reader.readtext(img_np)

    for detection in result:
        text = detection[1]
        if is_valid_plate(text):
            return text
    
    return "fail to detect number"

def is_valid_plate(text: str) -> bool:
    return any(char.isdigit() for char in text) and any(char.isalpha() for char in text)


def preprocess_image(img_np):
    # Grayscale
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # Histogram Equalization (명암 대비 향상)
    gray = cv2.equalizeHist(gray)
    
    # Thresholding or Adaptive
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh






