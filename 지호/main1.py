import os
import shutil
from pathlib import Path
from datetime import datetime


def fl():
    folder_path = input("정리할 폴더 경로를 입력하세요:")
    if not os.path.exists(folder_path):
        print("존재하지 않는 폴더 입니다.")
        return
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
        if os.path.isfile(full_path) and folder_name != "기타":
            os.makedirs(dst_path, exist_ok=True)
            shutil.move(full_path, dst_path)
            print(filename, folder_name)

    print("정리가 완료되었습니다.")


def day():
    folder = input("정리할 폴더 경로 입력 ")
    folder = Path(folder)
    if not folder.exists():
        print("존재하지 않는 폴더입니다.")
        return
    files = [f for f in folder.iterdir() if f.is_file()]
    for f in files:
        mtime = os.path.getmtime(f)
        year = datetime.fromtimestamp(mtime).strftime("%Y")
        year_folder = folder / year
        os.makedirs(year_folder, exist_ok=True)
        shutil.move(str(f), str(year_folder / f.name))
    print("정리가 완료되었습니다.")


# 메뉴
def main():
    while True:
        print("==== 파일 정리 자동화 ====")
        print("1. 확장자별 정리")
        print("2. 날짜별 정리")
        print("3. 종료")

        choice = input("번호 입력: ")

        if choice == "1":
            fl()
        elif choice == "2":
            day()
        elif choice == "3":break
        else:
            print("올바른 번호를 입력하세요")

main()