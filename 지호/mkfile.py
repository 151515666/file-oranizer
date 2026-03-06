import os
import shutil


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

    for filename in files:   #files리스트에서 파일 이름을 하나씩 꺼내 filename에 담기
        result = os.path.splitext(filename)  #파일 이름을 이름이랑 확장자로 쪼개기 예)사진1.jpg면 ('사진1', '.jpg')
        folder_name = extension_map.get(result[1], "기타") #result[1]로 확장자만 꺼내서 딕셔너리에 찾기 .jpg면 "사진" 없으면 "기타"
        full_path = os.path.join(folder_path, filename) #파일 전체 경로 만들기
        dst_path = os.path.join(folder_path, folder_name) #이동할 목적지 폴더 경로 만들기 /User/sadasd/file/사진 이런식

        if os.path.isfile(full_path) and folder_name != "기타":
            os.makedirs(dst_path, exist_ok=True)
            shutil.move(full_path, dst_path)
            print(filename, folder_name)
fl()