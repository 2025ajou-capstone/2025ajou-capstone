from typing import List

from ultralytics import YOLO

model = YOLO("best.pt")  # fine-tuned 모델 경로

def detect_yolo_objects(frame) -> List[str]:
    results = model(frame)
    return [d.name for d in results[0].boxes.cls]  # 객체 이름 리스트
