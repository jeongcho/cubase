from PIL import Image
import os

# 지정된 폴더 경로를 설정하세요
folder_path = os.getcwd()

# 삭제할 세로 방향 픽셀의 시작과 끝 지점
remove_start = 205 
remove_end = 470

# 폴더 내의 모든 .png 파일을 대상으로 반복
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # 이미지 파일의 전체 경로
        img_path = os.path.join(folder_path, filename)
        
        # 이미지 열기
        with Image.open(img_path) as img:
            # 이미지의 원래 크기를 가져옴
            width, height = img.size
            
            # 이미지를 잘라내기 전과 후로 나눔
            top_part = img.crop((0, 0, width, remove_start))
            bottom_part = img.crop((0, remove_end, width, height))
            
            # 새 이미지의 총 높이 계산
            new_height = remove_start + (height - remove_end)
            
            # 새 이미지 생성
            new_img = Image.new('RGB', (width, new_height))
            
            # 상단 부분 붙이기
            new_img.paste(top_part, (0, 0))
            
            # 하단 부분 붙이기
            new_img.paste(bottom_part, (0, remove_start))

            new_img_path = os.path.join(folder_path, '_' + filename)
            
            # 수정된 이미지를 원본 파일 이름으로 저장
            new_img.save(new_img_path)

print("모든 이미지가 수정되었습니다.")
