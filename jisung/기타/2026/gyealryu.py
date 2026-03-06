import os
import shutil
from pathlib import Path
from datetime import datetime
def day():
    folder = input("정리할 폴더 경로 입력 ")
    folder = Path(folder)

    if not folder.exists():
        print("존재하지 않는 폴더입니다.")
        return

    files = [f for f in folder.iterdir() if f.is_file()]

    #files = []  # 빈 리스트 만들기

    #for f in folder.iterdir():  # 폴더 안 항목을 하나씩 꺼내서
    #    if f.is_file():          # 파일이면 (폴더 제외)
    #        files.append(f)      # 리스트에 추가

    for f in files:
        mtime = os.path.getmtime(f)
        date = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

    year = datetime.fromtimestamp(mtime).strftime("%Y")

    for f in files:
        mtime = os.path.getmtime(f)
        year = datetime.fromtimestamp(mtime).strftime("%Y")
    
        year_folder = folder / year  # 년도 폴더 경로
        os.makedirs(year_folder, exist_ok=True)  # 폴더 없으면 생성
        shutil.move(str(f), str(year_folder / f.name))  # 파일 이동
    
    print("정리가 완료되었습니다.")
day()