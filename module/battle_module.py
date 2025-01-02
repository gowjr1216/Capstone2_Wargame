# battle_module.py
# 최적의 행동을 학습한 전투모듈 저장 코드

import sys
import os
import gym
from gym import spaces
import numpy as np
from stable_baselines3 import PPO
import time

# Soldier, AntiTank, Sniper, Drone, Medic, Airstrike 클래스를 불러오기 위한 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unit.unit import Soldier, AntiTank, Sniper, Drone, Medic, Airstrike

class BattleEnv(gym.Env):
    def __init__(self):
        super(BattleEnv, self).__init__()
        
        self.observation_space = spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)
        self.action_space = spaces.Discrete(7)  # 이동(4방향), 공격, 회복, 대기 등
        
        self.team1_units, self.team1_airstrike = self.create_team("Team1")
        self.team2_units, self.team2_airstrike = self.create_team("Team2")
        
        self.reset()

    def reset(self):
        self.state = np.random.rand(10)
        self.done = False
        self.steps = 0
        self.team1_survivors = len(self.team1_units)
        self.team2_survivors = len(self.team2_units)
        self.team1_morale = 100
        self.team2_morale = 100
        return self.state

    def create_team(self, team_name):
        team = [Soldier("일반병사", 100, 20, 10, 30, 1.0) for _ in range(50)]
        team.extend([Sniper() for _ in range(2)])
        team.extend([AntiTank() for _ in range(3)])
        team.append(Drone())
        team.append(Medic())  # 의무병
        team.extend([Soldier("통신병", 100, 10, 10, 30, 1.0, can_transmit=True) for _ in range(2)])  # 통신병
        return team, Airstrike()

    def step(self, action):
        reward = 0
        self.steps += 1

        # 유닛별로 최적화된 행동 수행
        for unit in self.team1_units:
            if isinstance(unit, Soldier) or isinstance(unit, AntiTank) or isinstance(unit, Sniper):
                # 일반병사, 대전차, 저격병사의 탐지 및 공격 처리
                if self.can_detect_enemy(unit):
                    target = self.find_target(unit, self.team2_units)
                    if target and self.can_attack(unit, target):
                        reward += self.attack_target(unit, target)
            elif isinstance(unit, Medic):
                # 의무병의 회복 행동
                if self.heal_ally(unit):
                    reward += 30
            elif isinstance(unit, Drone):
                # 드론의 최적화된 탐지 및 지원
                reward += self.handle_drone(unit)
            elif isinstance(unit, Airstrike):
                # 공습 지원
                reward += self.handle_airstrike(unit)

        # 팀의 사기 감소 및 속도 저하
        reward += self.update_morale()

        # 승리/패배 보상 및 패널티
        if self.team2_survivors <= 0:  # 승리 조건
            reward += 300
            self.done = True
        elif self.team1_survivors <= 0:  # 패배 조건
            reward -= 300
            self.done = True
        else:
            self.done = False  # 전투가 계속됨

        return self.state, reward, self.done, {}

    def can_detect_enemy(self, unit):
        """유닛이 시야 거리 및 시야각 내에서 적을 탐지할 수 있는지 확인"""
        for enemy in self.team2_units:
            distance = np.linalg.norm(np.array([unit.x, unit.y]) - np.array([enemy.x, enemy.y]))
            
            # 두 점 간의 각도 계산 (atan2 사용)
            angle_to_enemy = np.arctan2(enemy.y - unit.y, enemy.x - unit.x)
            
            if distance <= unit.vision and abs(unit.view_direction - angle_to_enemy) <= unit.view_angle / 2:
                return True
        return False

    def find_target(self, unit, enemies):
        """공격 가능한 범위 내에서 적을 찾아 반환"""
        for enemy in enemies:
            distance = np.linalg.norm(np.array([unit.x, unit.y]) - np.array([enemy.x, enemy.y]))
            if distance <= unit.range:
                return enemy
        return None

    def can_attack(self, unit, target):
        """장전 시간을 확인하여 공격 가능 여부를 판단"""
        return time.time() - unit.last_attack_time >= unit.reload_time

    def attack_target(self, unit, target):
        """공격하여 적의 체력을 감소시키고 보상을 반환"""
        damage = max(1, unit.attack_power - target.defense)
        target.health -= damage
        unit.last_attack_time = time.time()
        if target.health <= 0:
            self.team2_survivors -= 1
            return 50  # 적 처치 보상
        return 0

    def heal_ally(self, medic):
        """의무병이 아군의 체력을 회복"""
        for ally in self.team1_units:
            if ally.health < 50 and medic.healed_count < medic.heal_limit:
                ally.health += 20
                medic.healed_count += 1
                return True
        return False

    def handle_drone(self, drone):
        """드론 최적화된 행동 처리"""
        reward = 0
        # 드론이 적의 위치를 탐지하는 예시
        for enemy in self.team2_units:
            if np.linalg.norm(np.array([drone.x, drone.y]) - np.array([enemy.x, enemy.y])) <= drone.range:
                drone.detect_enemy(enemy)
                reward += 0.5  # 탐지 보상
        return reward

    def handle_airstrike(self, airstrike):
        """공습 지원 최적화된 행동 처리"""
        reward = 0
        # Airstrike 유닛이 공격하는 예시
        for enemy in self.team2_units:
            if np.linalg.norm(np.array([airstrike.x, airstrike.y]) - np.array([enemy.x, enemy.y])) <= airstrike.range:
                damage = airstrike.attack_power
                enemy.health -= damage
                reward += 1  # 공습 보상
        return reward

    def update_morale(self):
        """사기에 따른 속도 감소 및 보상/패널티 적용"""
        morale_penalty = 0
        if self.team1_survivors < len(self.team1_units) * 0.8:
            self.team1_morale -= 5  # 아군 사망에 따른 사기 저하
            morale_penalty -= 10  # 사기에 따른 속도 저하 보상
            for unit in self.team1_units:
                unit.speed *= 0.9  # 사기 저하로 인한 속도 감소
        return morale_penalty

def predict_enemy_path(self, soldier):
    """상대방의 이동 경로를 예측하고, 기습 공격을 위한 최적의 경로를 찾음"""
    reward = 0
    
    # 1. 적의 최근 이동 경로를 기록하고 추적
    enemy_paths = self.track_enemy_paths(soldier)
    
    # 2. 상대의 움직임 패턴을 분석하여 예측
    predicted_positions = self.analyze_enemy_movement(enemy_paths)
    
    # 3. 병사가 기습할 수 있는 최적의 경로 찾기
    ambush_position = self.find_ambush_position(soldier, predicted_positions)
    
    if ambush_position:
        # 4. 기습 공격을 위해 병사를 해당 위치로 이동
        reward += self.move_to_position(soldier, ambush_position)  # 기습 이동 보상
        
        # 5. 기습 공격
        target = self.find_target(soldier, self.team2_units)
        if target and self.can_attack(soldier, target):
            reward += self.attack_target(soldier, target)  # 기습 공격 보상
    
    return reward

def track_enemy_paths(self, soldier):
    """적의 경로 기록 및 추적"""
    paths = []
    for enemy in self.team2_units:
        path = []
        for step in range(1, self.steps):
            path.append((enemy.x + np.random.uniform(-2, 2), enemy.y + np.random.uniform(-2, 2)))  # 예시로 약간의 랜덤한 이동
        paths.append(path)
    return paths

def analyze_enemy_movement(self, enemy_paths):
    """적의 이동패턴 분석 및 예측"""
    predicted_positions = []
    for path in enemy_paths:
        if len(path) >= 3:
            recent_moves = path[-3:]
            avg_x = np.mean([move[0] for move in recent_moves])
            avg_y = np.mean([move[1] for move in recent_moves])
            predicted_positions.append((avg_x, avg_y))
    return predicted_positions

def find_ambush_position(self, soldier, predicted_positions):
    """기습"""
    min_distance = float('inf')
    ambush_position = None
    for predicted_position in predicted_positions:
        distance = np.linalg.norm(np.array([soldier.x, soldier.y]) - np.array(predicted_position))
        if distance < min_distance:
            min_distance = distance
            ambush_position = predicted_position
    return ambush_position



# 학습 실행
env = BattleEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# 전투모델 저장
obs = env.reset()
for _ in range(100):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()

# 모델 저장
model.save("battle_module.zip")  # 모델을 battle_module.zip으로 저장
print("battle_module.zip에 전투모듈 저장완료")

