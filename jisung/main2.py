import os
import shutil
from pathlib import Path
from datetime import datetime

def main2():
        folder = input("정리할 폴더 경로 입력 ")
        folder = Path(folder)

        if not folder.exists():
            print("존재하지 않는 폴더입니다.")
            return    

        extension_map = {
           ".jpg": "사진",
            ".png": "사진",
           ".mp3": "음악",
            ".docx": "문서",
            ".xlsx": "문서",
            ".pdf": "문서",
           ".mp4": "영상",
      }

        files = [f for f in folder.iterdir() if f.is_file()]

        for f in files:
            category = extension_map.get(f.suffix, "기타")

            mtime = os.path.getmtime(f)
            year = datetime.fromtimestamp(mtime).strftime("%Y")

            dst_folder = folder / category / year
            os.makedirs(dst_folder, exist_ok=True)  
            shutil.move(str(f), str(dst_folder / f.name))
        print("정리가 완료되었습니다.")
main2()