import os
import cv2
import sys

# 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from vision.object_detect import detect_yolo_objects

# 영상 경로 지정
video_path = os.path.join(BASE_DIR, "media", "20250413_093718_1.mp4")
if not os.path.exists(video_path):
    print(f"❌ Video not found: {video_path}")
    exit(1)

# 영상 로드
cap = cv2.VideoCapture(video_path)
frame_idx = 0

while cap.isOpened():
    frame_idx += 1
    ret, frame = cap.read()
    # frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)   
    if frame_idx % 10 == 0:
        save_dir = os.path.join(BASE_DIR, "captured_frames")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"image_{frame_idx}.jpg")
        cv2.imwrite(save_path, frame)

    # print("frame shape:", frame.shape)  # (height, width, channels)
    if not ret:
        break

    # if frame_idx == 30:
    #     break

    
    if frame_idx % 5 in [1,2,3,4]:
        continue
    # # YOLO 감지
    # objects = detect_yolo_objects(frame)

    # # 결과 시각화
    # for obj in objects:
    #     x1, y1, x2, y2 = obj["xyxy"]
    #     label = obj["label"]
    #     score = obj["score"]

    #     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    #     cv2.putText(frame, f"{label} {score:.2f}", (x1, y1 - 10),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # # 프레임 표시
    cv2.imshow("YOLO Detection", frame)

    if cv2.waitKey(30) & 0xFF == 27:  # ESC 키 누르면 종료
        break



cap.release()
cv2.destroyAllWindows()
