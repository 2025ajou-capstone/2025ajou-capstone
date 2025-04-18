import cv2
import numpy as np
from collections import deque
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

def lane_detection(image):

    def convert_hls(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

    def applied_Gaussian(image, kerner_size=15):
        return cv2.GaussianBlur(image, (kerner_size, kerner_size), 0)

    def detected_Canny(image, low_threshold=50, high_threshold=150):
        return cv2.Canny(image, low_threshold, high_threshold)

    def White_Yellow_Detection(image):
        converted = convert_hls(image)
        white_lower = np.uint8([0, 200, 0])
        white_upper = np.uint8([255, 255, 255])
        white_mask = cv2.inRange(converted, white_lower, white_upper)

        yellow_lower = np.uint8([10, 0, 100])
        yellow_upper = np.uint8([40, 255, 255])
        yellow_mask = cv2.inRange(converted, yellow_lower, yellow_upper)

        mask = cv2.bitwise_or(white_mask, yellow_mask)
        return cv2.bitwise_and(image, image, mask=mask)

    def filter_region(image, vertices):
        mask = np.zeros_like(image)
        if len(mask.shape) == 2:
            cv2.fillPoly(mask, vertices, 255)
        else:
            cv2.fillPoly(mask, vertices, (255,) * mask.shape[2])
        return cv2.bitwise_and(image, mask)

    def region_of_interest(image):
        height, width = image.shape[:2]
        vertices = np.array([[
            [width * 0.1, height * 0.95],
            [width * 0.4, height * 0.6],
            [width * 0.6, height * 0.6],
            [width * 0.9, height * 0.95]
        ]], dtype=np.int32)
        return filter_region(image, vertices)

    def hough_transform(image):
        return cv2.HoughLinesP(image, rho=1, theta=np.pi/180, threshold=20, minLineLength=20, maxLineGap=30)

    def make_line_points(image, lines_parameters):
        try:
            slope, intercept = lines_parameters
            if abs(slope) < 1e-2:
                raise ValueError("Slope too small")
        except (TypeError, ValueError):
            return np.array([0, 0, 0, 0])

        y1 = int(image.shape[0])
        y2 = int(y1 * 0.6)
        try:
            x1 = int((y1 - intercept) / slope)
            x2 = int((y2 - intercept) / slope)
        except ZeroDivisionError:
            return np.array([0, 0, 0, 0])
        return np.array([x1, y1, x2, y2])

    def average_slope_intercept(image, lines):
        left_fit = []
        right_fit = []
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            if abs(slope) < 0.3:
                continue
            if slope < 0:
                left_fit.append((slope, intercept))
            else:
                right_fit.append((slope, intercept))

        left_line = make_line_points(image, np.average(left_fit, axis=0)) if left_fit else np.array([0, 0, 0, 0])
        right_line = make_line_points(image, np.average(right_fit, axis=0)) if right_fit else np.array([0, 0, 0, 0])

        return np.array([left_line, right_line])

    def draw_lane_lines(image, lines, color=[0, 0, 255], thickness=5):
        line_image = np.zeros_like(image)
        if lines is not None:
            for x1, y1, x2, y2 in lines:
                if x1 == x2 == y1 == y2 == 0:
                    continue
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
        return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)

    def center_line(image, lines):
        line_image = np.zeros_like(image)

        x1_1, y1_1, x2_1, y2_1 = lines[0].flatten().tolist()
        x1_2, y1_2, x2_2, y2_2 = lines[1].flatten().tolist()

        # 비정상 값 방어
        if any(abs(val) > 2000 for val in [x1_1, y1_1, x2_1, y2_1, x1_2, y1_2, x2_2, y2_2]):
            print("🚨 이상치 포함된 라인 감지, center_line 그리지 않음")
            return image

        xm1 = int((x1_1 + x1_2) / 2)
        xm2 = int((x2_1 + x2_2) / 2)
        ym1 = int((y1_1 + y1_2) / 2)
        ym2 = int((y2_1 + y2_2) / 2)

        cv2.line(line_image, (xm1, ym1), (xm2, ym2), color=(0, 255, 0), thickness=10)
        return cv2.addWeighted(image, 1.0, line_image, 0.95, 0.0)

    # 전체 파이프라인
    lane_image = np.copy(image)
    white_yellow_frame = White_Yellow_Detection(lane_image)
    Gaussian_frame = applied_Gaussian(white_yellow_frame)
    Canny_frame = detected_Canny(Gaussian_frame)
    roi_frame = region_of_interest(Canny_frame)
    hough_frame = hough_transform(roi_frame)

    if hough_frame is None or len(hough_frame) < 2:
        print("⚠️ 차선 부족 - 라인 생략")
        return image

    average_line_frame = average_slope_intercept(image, hough_frame)
    center_image = center_line(lane_image, average_line_frame)
    result_image = draw_lane_lines(center_image, average_line_frame)
    return result_image

# 영상 처리 루프
video_path = os.path.join(BASE_DIR, "media", "20250413_093718_1.mp4")
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    result = lane_detection(frame)
    cv2.imshow('Original', frame)
    cv2.imshow('result', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
