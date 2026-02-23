import os
import shutil

# 현재 디렉토리 출력
# print(os.getcwd())

# 현재경로에 파일 만들기
# os.mkdir("/Users/jiho/file-oranizer/test_mkdir")

# 현재 디렉토리 내의 모든 파일과 폴더명 리스트로 변환
# os.listdir("/디렉토리")
# print(os.listdir(os.getcwd()))

# 확장자 출력하는법
# result = os.path.splitext("사진1.jpg")
# print(result[1])

folder_path = "/Users/jiho/file-oranizer"
files = os.listdir(folder_path)
extension_map = {
    ".jpg": "사진",
    ".png": "사진",
    ".mp3": "음악",
    ".docx": "문서",
    ".xlsx": "문서",
    ".pdf": "문서",
    ".mp4": "영상",
}

for filename in files:
    result = os.path.splitext(filename)
    folder_name = extension_map.get(result[1], "기타")
    full_path = os.path.join(folder_path, filename)
    dst_path = os.path.join(folder_path, folder_name)

    if os.path.isfile(full_path):
        shutil.move(full_path, dst_path)
        print(filename, folder_name)

