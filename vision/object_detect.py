from typing import List
import os

from ultralytics import YOLO


# model = YOLO(r"./models/0409_plate_detect_v1.pt")  # fine-tuned 모델 경로
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(ROOT_DIR, 'models', '250413_fine_tuning.pt')
model = YOLO(model_path)

# class YOLOV2():
#     instance = None

#     @classmethod
#     def get_instance(cls):
#         if not cls.instance:
#             print("Creating new YOLOV2 instance")
#             cls.instance = YOLO(model_path)
#         return cls.instance

#     @classmethod
#     def detect(cls, frame, imgsz):
#         instance = cls.get_instance()  # 첫 호출 시 인스턴스를 생성
#         return instance(frame, imgsz)

def detect_yolo_objects(frame):
    results = model(frame, imgsz = 1024)
    names = model.names
    boxes = results[0].boxes

    detected = []
    if boxes is not None:
        for i in range(len(boxes.cls)):
            cls_id = int(boxes.cls[i])
            conf = float(boxes.conf[i])
            x1, y1, x2, y2 = map(int, boxes.xyxy[i])
            detected.append({
                "label": names[cls_id],
                "score": conf,
                "xyxy": (x1, y1, x2, y2)
            })

    return detected
