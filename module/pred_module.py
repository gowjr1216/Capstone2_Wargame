# pred_module.py
# 시뮬레이션 데이터를 이용한 예측모듈 생성 코드

import sys
import os
import gzip  # gzip 추가
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib  # 모델 저장/로드를 위한 joblib
import time  # 진행률 출력 간 지연을 위한 모듈

# 'unit' 폴더 경로를 sys.path에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../unit')))

# data.pkl.gz 파일 로드
try:
    with gzip.open('data.pkl.gz', 'rb') as file:
        results = pickle.load(file)
    print("data.pkl.gz 파일 로드 성공!")
except Exception as e:
    print(f"data.pkl.gz 파일 로드 실패: {e}")
    sys.exit(1)

# 데이터 키 확인
print("데이터 키:", results.keys())

# 실제 전투 데이터를 기반으로 학습 데이터 생성
data = []
total_samples = 50  # 생성할 샘플 수

for i in range(total_samples):  # 50개의 가상 샘플 생성
    try:
        # 가상 데이터 생성
        team1_loss_rate = results["average_team1_loss_rate"] + i * 0.2
        team2_loss_rate = results["average_team2_loss_rate"] + i * 0.1
        time_step = results.get("average_time", 100) + i * 2  # 'average_time' 키가 없을 경우 기본값 100 사용
        team1_win = 1 if i % 2 == 0 else 0  # 번갈아 승패 설정
        data.append({
            "team1_loss_rate": team1_loss_rate,
            "team2_loss_rate": team2_loss_rate,
            "time_step": time_step,
            "team1_win": team1_win
        })
        # 진행률 출력
        print(f"진행률: {(i + 1) / total_samples * 100:.1f}%")
        time.sleep(0.1)  # 진행률 출력 간 지연
    except KeyError as e:
        print(f"데이터 생성 중 키 오류 발생: {e}")
        sys.exit(1)

# DataFrame 생성
df = pd.DataFrame(data)
print("\n학습 데이터 생성 완료!")
print(df.head())  # 샘플 데이터 확인

# 특성(Feature)와 레이블(Label) 설정
X = df[["team1_loss_rate", "team2_loss_rate", "time_step"]]  # 특성
y = df["team1_win"]  # 레이블

# 로지스틱 회귀 모델 학습
try:
    print("\n로지스틱 회귀 모델 학습 중...")
    model = LogisticRegression(max_iter=10000, C=0.1)
    model.fit(X, y)
    print("모델 학습 완료!")
except Exception as e:
    print(f"모델 학습 중 오류 발생: {e}")
    sys.exit(1)

# 모델 저장
try:
    joblib.dump(model, 'pred_module.zip')
    print("모델 저장 완료: pred_module.zip")
except Exception as e:
    print(f"모델 저장 중 오류 발생: {e}")
