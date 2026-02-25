import os
import shutil
from pathlib import Path

folder = input("정리할 폴더 경로 입력")
folder = Path(folder)

if not folder.exists():
    print("존재하지 않는 폴더입니다.")
    exit()

#files = [f for f in folder.iterdir() if f.is_file()]

#files = []   빈 리스트 만들기

#for f in folder.iterdir():   폴더 안 항목을 하나씩 꺼내서
#    if f.is_file():           파일이면 (폴더 제외)
#        files.append(f)       리스트에 추가