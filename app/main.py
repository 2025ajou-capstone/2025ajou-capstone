from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from PIL import Image, UnidentifiedImageError
import numpy as np
from io import BytesIO
import cv2
import sys

# root 디렉토리 경로
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


sys.path.append(BASE_DIR)


from vision.ocr import detect_plate_number
from vision.object_detect import detect_yolo_objects

app = FastAPI()

static_dir = os.path.join(BASE_DIR, "static")
media_dir = os.path.join(BASE_DIR, "media")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
if os.path.exists(media_dir):
    app.mount("/media", StaticFiles(directory=media_dir), name="media")

@app.get("/")
async def root():
    index_path = os.path.join(BASE_DIR, "static", "index.html")
    with open(index_path, encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/video")
async def upload_video(file: UploadFile = File(...)):
    # save file
    os.makedirs("media", exist_ok = True)
    video_path = f"media/{file.filename}"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # get frame
    cap = cv2.VideoCapture(video_path)
    results = []

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_idx > 30:   # test로 30 frame만
            break

        detected = detect_yolo_objects(frame)   # module 만들어서 연결하기기
        results.append({
            "frame": frame_idx,
            "objects": detected
        })
        frame_idx += 1
    
    cap.release()
    return JSONResponse({"result": "success", "frames_analyzed": frame_idx, "detections": results})





@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 파일 전체 읽기 (bytes)
        contents = await file.read()

        # 저장
        os.makedirs("media", exist_ok=True)
        save_path = f"media/{file.filename}"
        with open(save_path, "wb") as f:
            f.write(contents)  # ✅ 이미 읽은 contents를 저장

        # 이미지 열기
        image = Image.open(BytesIO(contents)).convert("RGB")
        image_np = np.array(image)
        print(f"이미지 shape: {image_np.shape}")

        plate_number = detect_plate_number(image_np)
        print(f"detected car number: {plate_number}")



        return JSONResponse({"result": "success", "plate_number": plate_number})

    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="이미지 파일 형식을 인식할 수 없습니다.")
