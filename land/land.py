# land.py
# 지형데이터

import numpy as np
import pickle
from noise import snoise2
import random

def generate_terrain(size, offset_x, offset_y):
    terrain_map = np.zeros((size, size), dtype=int)
    for i in range(size):
        for j in range(size):
            # 노이즈 파라미터를 조정하여 덜 복잡한 지형을 생성
            noise_value = snoise2((i + offset_x) / 200.0, (j + offset_y) / 200.0, octaves=2, persistence=0.4, lacunarity=1.5)
            # 지형 범위를 조정하여 다양한 지형이 나타나도록 설정
            if noise_value < -0.3:
                terrain_map[i][j] = 220  # 산악 (진한 회색)
            elif noise_value < -0.1:
                terrain_map[i][j] = 180  # 숲 (중간 회색)
            elif noise_value < 0.1:
                terrain_map[i][j] = 140  # 평지 (옅은 회색)
            elif noise_value < 0.3:
                terrain_map[i][j] = 100  # 도시 (더 옅은 회색)
            else:
                terrain_map[i][j] = 255  # 강 (흰색)
    return terrain_map

def save_terrain(filename, num_maps=20, size=1000):  # size를 1000으로 줄임
    all_terrains = []
    for _ in range(num_maps):
        offset_x = random.randint(0, 10000)
        offset_y = random.randint(0, 10000)
        terrain_map = generate_terrain(size, offset_x, offset_y)
        all_terrains.append(terrain_map)

    with open(filename, 'wb') as file:
        pickle.dump(all_terrains, file)
    print(f"{filename} 파일에 모든 지형 데이터가 저장되었습니다.")

if __name__ == "__main__":
    save_terrain("land.pkl", num_maps=20, size=1000)  # size를 1000으로 설정
