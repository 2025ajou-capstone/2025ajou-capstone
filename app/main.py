from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from PIL import Image, UnidentifiedImageError
import numpy as np
from io import BytesIO

from ml_model.ocr import detect_plate_number



app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
async def root():
    return HTMLResponse(content=open("static/index.html", encoding="utf-8").read())


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
