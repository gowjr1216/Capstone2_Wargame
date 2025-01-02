# dland.py
# land.pkl을 보여주는 코드

import pickle
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import os

def display_all_terrains(filename):
    with open(filename, 'rb') as file:
        terrains = pickle.load(file)
    
    root = tk.Tk()
    root.title("전체 지형 시각화")
    
    # 모든 지형을 10x10 그리드로 배치
    rows, cols = 10, 10
    thumb_size = 80  # 각 썸네일 크기 조정

    for idx, terrain_map in enumerate(terrains):
        row = idx // cols
        col = idx % cols

        # 지형을 이미지로 변환하고 크기 조정
        image = Image.fromarray(np.uint8(terrain_map), 'L').resize((thumb_size, thumb_size))
        img_tk = ImageTk.PhotoImage(image=image)
        
        # 이미지 라벨을 그리드에 추가
        label = tk.Label(root, image=img_tk)
        label.image = img_tk  # 이미지 참조 유지
        label.grid(row=row, column=col, padx=2, pady=2)  # 격자 형태로 배치

    root.mainloop()

if __name__ == "__main__":
    # 현재 스크립트의 디렉토리를 기준으로 상대 경로 설정
    base_dir = os.path.dirname(__file__)  # 현재 파일의 디렉토리
    filename = os.path.join(base_dir, "..", "land", "land.pkl")  # 한 단계 위로 올라가 land 폴더 참조
    display_all_terrains(filename)
