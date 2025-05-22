from PIL import Image
import os

# 지정된 폴더 경로를 설정하세요
folder_path = os.getcwd()

# 폴더 내의 모든 .png 파일을 대상으로 반복
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # 이미지 파일의 전체 경로
        img_path = os.path.join(folder_path, filename)
        
        # 이미지 열기
        with Image.open(img_path) as img:
            # 이미지의 원래 크기를 가져옴
            width, height = img.size
            
            # 좌우에서 2픽셀, 상하에서 3픽셀 잘라냄
            # (왼쪽, 위, 오른쪽, 아래)
            left = 0
            top = 1080-425
            right = width - 0
            bottom = height - 0
            
            # 이미지를 잘라냄
            cropped_img = img.crop((left, top, right, bottom))
            
            # 수정된 이미지를 원본 파일 이름으로 저장
            cropped_img.save(img_path)

print("모든 이미지가 수정되었습니다.")
