import os
import shutil
from pathlib import Path
from datetime import datetime


EXTENSION_MAP = {
    ".jpg": "사진",
    ".jpeg": "사진",
    ".png": "사진",
    ".gif": "사진",
    ".mp3": "음악",
    ".wav": "음악",
    ".flac": "음악",
    ".docx": "문서",
    ".xlsx": "문서",
    ".pdf": "문서",
    ".pptx": "문서",
    ".txt": "문서",
    ".mp4": "영상",
    ".mov": "영상",
    ".avi": "영상",
}


def resolve_duplicate(dst_folder: Path, filename: str) -> Path:
    """같은 이름 파일이 있으면 (1), (2)... 붙여서 반환"""
    dst = dst_folder / filename
    if not dst.exists():
        return dst
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while dst.exists():
        dst = dst_folder / f"{stem}({counter}){suffix}"
        counter += 1
    return dst


def organize_by_extension():
    folder = Path(input("정리할 폴더 경로를 입력하세요: ").strip())
    if not folder.exists():
        print("존재하지 않는 폴더입니다.")
        return

    moved = 0
    for f in folder.iterdir():
        if not f.is_file():
            continue
        folder_name = EXTENSION_MAP.get(f.suffix.lower(), "기타")
        dst_folder = folder / folder_name
        dst_folder.mkdir(exist_ok=True)
        dst = resolve_duplicate(dst_folder, f.name)
        shutil.move(str(f), str(dst))
        print(f"{f.name} → {folder_name}/{dst.name}")
        moved += 1

    print(f"\n정리 완료: {moved}개 파일 이동")


def organize_by_date():
    folder = Path(input("정리할 폴더 경로를 입력하세요: ").strip())
    if not folder.exists():
        print("존재하지 않는 폴더입니다.")
        return

    moved = 0
    for f in folder.iterdir():
        if not f.is_file():
            continue
        mtime = os.path.getmtime(f)
        year = datetime.fromtimestamp(mtime).strftime("%Y")
        year_folder = folder / year
        year_folder.mkdir(exist_ok=True)
        dst = resolve_duplicate(year_folder, f.name)
        shutil.move(str(f), str(dst))
        print(f"{f.name} → {year}/{dst.name}")
        moved += 1

    print(f"\n정리 완료: {moved}개 파일 이동")


def main():
    while True:
        print("\n==== 파일 정리 자동화 ====")
        print("1. 확장자별 정리")
        print("2. 날짜별 정리")
        print("3. 종료")

        choice = input("번호 입력: ").strip()

        if choice == "1":
            organize_by_extension()
        elif choice == "2":
            organize_by_date()
        elif choice == "3":
            print("종료합니다.")
            break
        else:
            print("올바른 번호를 입력하세요.")


main()
