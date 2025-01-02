# data.py
# team1 vs team2 의 1000번의 시뮬레이션 데이터 저장 코드

import gzip
import pickle
import random
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unit.unit import Unit  # Unit 클래스를 별도 파일에서 가져옵니다.

land_path = '../land/land.pkl'
unit_path = '../unit/unit.pkl'

def load_data():
    with open(land_path, 'rb') as file:
        lands = pickle.load(file)
    with open(unit_path, 'rb') as file:
        units = pickle.load(file)
    return random.choice(lands), units

def place_units_on_map(terrain, team_units, team_color, position="top_left"):
    positions = []
    size = len(terrain)
    offset = size // 5

    start_x, start_y = (0, 0) if position == "top_left" else (size - offset, size - offset)
    for unit in team_units:
        while True:
            x = random.randint(start_x, start_x + offset - 1)
            y = random.randint(start_y, start_y + offset - 1)
            if terrain[x][y] != 255:  # 강이 아닌 곳에 배치
                positions.append([x, y, unit, team_color])
                break
    return positions

def simulate_battle():
    terrain, units = load_data()
    size = len(terrain)
    unit_positions = {
        'Team1': place_units_on_map(terrain, units['Team1'], 'blue', position="top_left"),
        'Team2': place_units_on_map(terrain, units['Team2'], 'red', position="bottom_right")
    }
    team1_survivors, team2_survivors = len(unit_positions['Team1']), len(unit_positions['Team2'])
    time_step = 0
    enemy_report_team1, enemy_report_team2 = [], []

    action_log = {'Team1': [], 'Team2': []}

    while team1_survivors > 0 and team2_survivors > 0:
        time_step += 1

        for team, units in unit_positions.items():
            other_team = 'Team2' if team == 'Team1' else 'Team1'
            enemy_report = enemy_report_team1 if team == 'Team1' else enemy_report_team2

            if not unit_positions[other_team]:  # 상대팀 유닛이 모두 사라지면 전투 종료
                return "Team1" if team2_survivors == 0 else "Team2", time_step, action_log

            for pos in units:
                if pos[2].role == "통신병사" and pos[2].can_transmit:
                    enemy_report = [(p[0], p[1]) for p in unit_positions[other_team]]

            for pos in units:
                x, y, unit, color = pos
                if not unit_positions[other_team]:
                    break

                if enemy_report:
                    target_candidates = enemy_report
                else:
                    target_candidates = [(p[0], p[1]) for p in unit_positions[other_team]]

                if not target_candidates:
                    continue

                target = random.choice(target_candidates)
                target_x, target_y = target[0], target[1]
                move_x = 1 if target_x > x else -1 if target_x < x else 0
                move_y = 1 if target_y > y else -1 if target_y < y else 0
                pos[0] = max(0, min(size - 1, pos[0] + move_x))
                pos[1] = max(0, min(size - 1, pos[1] + move_y))

                distance = ((x - target_x) ** 2 + (y - target_y) ** 2) ** 0.5
                if distance <= unit.range:
                    other_unit = next((u for u in unit_positions[other_team] if (u[0], u[1]) == (target_x, target_y)), None)
                    if other_unit:
                        other_unit[2].health -= max(1, unit.attack - other_unit[2].defense)
                        if other_unit[2].health <= 0:
                            unit_positions[other_team].remove(other_unit)
                            if other_team == 'Team1':
                                team1_survivors -= 1
                            else:
                                team2_survivors -= 1

                action_log[team].append({
                    'unit_role': unit.role,
                    'position': (pos[0], pos[1]),
                    'target_position': (target_x, target_y),
                    'action': 'attack' if distance <= unit.range else 'move'
                })

    return "Team1" if team2_survivors == 0 else "Team2", time_step, action_log

def reinforcement_learning(num_simulations=1000, save_path="data.pkl.gz"):  # 압축 파일로 저장
    results = {"Team1": 0, "Team2": 0, "time_steps": [], "action_logs": []}

    for i in range(num_simulations):
        result, time_step, action_log = simulate_battle()
        results[result] += 1
        results["time_steps"].append(time_step)
        results["action_logs"].append(action_log)

        # 3초마다 진행률 출력
        print(f"진행률: {(i + 1) / num_simulations * 100:.1f}%")
        time.sleep(3)  # 3초 지연

    learning_data = {
        "wins": results["Team1"],
        "average_time": sum(results["time_steps"]) / num_simulations,
        "action_logs": results["action_logs"]
    }

    # gzip으로 압축 저장
    with gzip.open(save_path, 'wb') as file:
        pickle.dump(learning_data, file)

    print(f"{save_path}에 학습 결과 저장 완료")
    print(f"Team1 승리 횟수: {results['Team1']}")
    print(f"Team2 승리 횟수: {results['Team2']}")
    print(f"평균 전투 시간: {learning_data['average_time']:.2f} steps")

if __name__ == "__main__":
    reinforcement_learning()
