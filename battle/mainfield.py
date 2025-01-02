# mainfield.py
# 전투, 예측모듈과 유닛, 지형데이터를 활용한 실제 예측 코드

import os
import pickle
import random
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# 경로 설정
unit_path = "../unit/unit.pkl"
land_path = "../land/land.pkl"
battle_module_path = "../module/battle_module.zip"
pred_module_path = "../module/pred_module.zip"

# 데이터 로드 함수
def load_data():
    with open(unit_path, "rb") as unit_file, open(land_path, "rb") as land_file:
        units = pickle.load(unit_file)
        terrain = random.choice(pickle.load(land_file))  # 랜덤한 전투 지형 선택
    return units, terrain

# 전투 시뮬레이션 함수
def simulate_battle(team1_units, team2_units, terrain, battle_model):
    team1_loss = 0
    team2_loss = 0
    time_step = 0

    # Team1에 battle_module.zip 전략 적용
    for unit in team1_units:
        unit["health"] *= 1.1  # Team1 유닛의 체력 10% 강화 (예시 전략)
        unit["attack"] *= 1.2  # Team1 유닛의 공격력 20% 강화

    # 단순 전투 시뮬레이션 로직
    while team1_units and team2_units:
        time_step += 1

        # Team1과 Team2의 손실 계산
        team1_loss += sum(1 for unit in team1_units if unit["health"] <= 0)
        team2_loss += sum(1 for unit in team2_units if unit["health"] <= 0)

        # 랜덤으로 유닛 제거 (간단한 전투 시뮬레이션 예시)
        if random.random() < 0.5:
            team1_units.pop()  # Team1 손실
        if random.random() < 0.5:
            team2_units.pop()  # Team2 손실

        # 최대 100 스텝까지만 진행
        if time_step > 100:
            break

    # 손실률 계산
    team1_loss_rate = team1_loss / (team1_loss + len(team1_units)) * 100
    team2_loss_rate = team2_loss / (team2_loss + len(team2_units)) * 100

    return team1_loss_rate, team2_loss_rate, time_step

# 예측 함수
def predict_battle_result(team1_loss_rate, team2_loss_rate, time_step, pred_model):
    new_battle = {
        "team1_loss_rate": team1_loss_rate,
        "team2_loss_rate": team2_loss_rate,
        "time_step": time_step
    }
    new_data = pd.DataFrame([new_battle])
    predicted_result = pred_model.predict(new_data)
    predicted_proba = pred_model.predict_proba(new_data)

    print("\n=== 예측 결과 ===")
    print(f"예측된 승리 팀: {'Team 1' if predicted_result[0] == 1 else 'Team 2'}")
    print(f"Team 1 승리 확률: {predicted_proba[0][1] * 100:.2f}%")
    print(f"Team 2 승리 확률: {predicted_proba[0][0] * 100:.2f}%")
    print("\n=== 입력된 손실률 ===")
    print(f"Team 1 손실률: {new_battle['team1_loss_rate']}%")
    print(f"Team 2 손실률: {new_battle['team2_loss_rate']}%")
    print(f"Time Step: {new_battle['time_step']}")

# 메인 실행 코드
if __name__ == "__main__":
    # 데이터 로드
    units, terrain = load_data()
    team1_units = units["Team1"]
    team2_units = units["Team2"]

    # battle_module.zip 로드 (Team1 전략 적용)
    if os.path.exists(battle_module_path):
        battle_model = joblib.load(battle_module_path)
        print("전투 모듈(battle_module.zip)이 로드되었습니다.")
    else:
        print("전투 모듈(battle_module.zip)이 존재하지 않습니다.")
        exit()

    # pred_module.zip 로드 (예측 모델)
    if os.path.exists(pred_module_path):
        pred_model = joblib.load(pred_module_path)
        print("예측 모듈(pred_module.zip)이 로드되었습니다.")
    else:
        print("예측 모듈(pred_module.zip)이 존재하지 않습니다.")
        exit()

    # 전투 시뮬레이션 실행
    team1_loss_rate, team2_loss_rate, time_step = simulate_battle(
        team1_units, team2_units, terrain, battle_model
    )

    # 예측 결과 출력
    predict_battle_result(team1_loss_rate, team2_loss_rate, time_step, pred_model)
