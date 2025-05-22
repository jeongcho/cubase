import os
import cv2
import numpy as np
import re


def extract_last_part(filename):
    match = re.search(r'(\d{8}_\d{6}\.\d+\.png)$', filename)  # 'YYYYMMDD_HHMMSS.xxx.png' 패턴 추출
    return match.group(1) if match else filename  # 패턴이 맞으면 해당 부분만 사용, 없으면 원본 유지


# 🔹 1. 파일이 있는 폴더 경로 설정
# folder_path = r"C:\Users\jeong\AppData\Roaming\PotPlayer64\Capture"
folder_path = os.getcwd()

output_folder = r"d:\output"

# 폴더가 없으면 생성
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 🔹 2. 파일명을 ASCII 형식으로 변경 (공백 및 특수 문자 제거)
for filename in os.listdir(folder_path):
    old_path = os.path.join(folder_path, filename)

    # 새로운 파일명 생성 (한글 및 특수문자는 `_`로 변경)
    new_filename = "".join(c if c.isalnum() or c in "._-" else "_" for c in filename)
    new_path = os.path.join(folder_path, new_filename)

    # 파일명이 변경된 경우 rename 실행
    if old_path != new_path:
        print(f"Renaming: {old_path} -> {new_path}")
        os.rename(old_path, new_path)

# 🔹 3. 파일을 불러와서 하얀색 배경 제거 및 크롭
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        img_path = os.path.join(folder_path, filename)

        # 파일 존재 여부 확인
        if not os.path.exists(img_path):
            print(f"File not found: {img_path}")
            continue

        # 한글 파일명 지원을 위해 바이너리로 읽고 OpenCV에서 디코딩
        with open(img_path, "rb") as f:
            file_bytes = np.asarray(bytearray(f.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # 이미지가 제대로 로드되었는지 확인
        if image is None:
            print(f"Failed to load image: {img_path}")
            continue

        print(f"Processing: {img_path}")

        # 🔹 4. 하얀색 배경 제거 (배경이 흰색인지 확인하는 임계값)
        th = 150
        white_mask = np.all(image >= [th, th, th], axis=-1)

        # 하얀색 픽셀을 검정색으로 변경
        image[white_mask] = [0, 0, 0]

        # 하얀색이 아닌 픽셀을 흰색으로 변경
        image[~white_mask] = [255, 255, 255]

        # 🔹 5. 검정색 영역의 경계 찾기
        contours, _ = cv2.findContours(white_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 최소 경계 상자 계산
        min_x, min_y = image.shape[1], image.shape[0]
        max_x = max_y = 0

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            min_x, min_y = min(x, min_x), min(y, min_y)
            max_x, max_y = max(x + w, max_x), max(y + h, max_y)

        # 여백 추가
        padding = 20
        min_x = max(min_x - padding, 0)
        min_y = max(min_y - padding, 0)
        max_x = min(max_x + padding, image.shape[1])
        max_y = min(max_y + padding, image.shape[0])

        # 🔹 6. 이미지 크롭
        cropped_image = image[min_y:max_y, min_x:max_x]

        # 크롭된 이미지가 비어 있는 경우 방지
        if cropped_image is None or cropped_image.size == 0:
            print(f"❌ Error: Cropped image is empty! Skipping: {filename}")
            continue

        # # 결과 확인
        # cv2.imshow("Cropped Image", cropped_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 🔹 7. 저장 (파일명 인코딩 문제 해결)
        new_filename = extract_last_part(filename)  # 파일명에서 날짜 부분만 추출
        new_img_path = os.path.join(output_folder, new_filename)

        success = cv2.imwrite(new_img_path, cropped_image)

        if success:
            print(f"✅ Successfully saved: {new_img_path}")
        else:
            print(f"❌ Failed to save image: {new_img_path}")

