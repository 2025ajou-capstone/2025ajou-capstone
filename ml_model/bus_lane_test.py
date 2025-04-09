import cv2
import numpy as np

# 이미지 불러오기
image = cv2.imread('../media/test2.jpg')
if image is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

# 이미지 크기
height, width = image.shape[:2]
roi = image[height // 2:, :]

# HSV 변환
hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

# 하늘색 범위 설정 (하얀색·진한 파랑 제외)
lower_blue = np.array([90, 80, 120])
upper_blue = np.array([105, 220, 230])
# 하늘색 HSV 마스크
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 마스크 팽창
kernel = np.ones((3, 3), np.uint8)
blue_mask = cv2.dilate(blue_mask, kernel, iterations=1)

# 작은 영역 제거
num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(blue_mask)
filtered_mask = np.zeros_like(blue_mask)
min_area = 250  # 조절 가능 (100~1000 범위 추천)

for i in range(1, num_labels):
    if stats[i, cv2.CC_STAT_AREA] >= min_area:
        filtered_mask[labels == i] = 255

# 노란색 오버레이 생성
overlay = np.zeros_like(roi)
overlay[filtered_mask > 0] = (0, 255, 255)

# 합성
highlighted_roi = cv2.addWeighted(roi, 0.4, overlay, 0.6, 0)
output = image.copy()
output[height // 2:, :] = highlighted_roi

# 결과 출력
cv2.imshow('Sky-Blue Area Highlighted', output)
cv2.imshow('Blue Mask', blue_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
