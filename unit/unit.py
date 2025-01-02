# unit.py
# 유닛데이터

import pickle
import random
import time

class Unit:
    def __init__(self, role, health, attack, defense, range, speed, vision=50, can_transmit=False, 
                 view_angle=120, view_direction=0, attack_power=10, support_ability=False, grenade=False, 
                 morale=100, heal_limit=0, reload_time=1, x=0, y=0, armor=False, recon_range=0, 
                 surveillance_equipment=False, is_ship=False):  # is_ship을 추가
        self.role = role
        self.health = health
        self.attack = attack
        self.defense = defense
        self.range = range
        self.speed = speed
        self.vision = vision
        self.can_transmit = can_transmit
        self.view_angle = view_angle
        self.view_direction = view_direction
        self.attack_power = attack_power
        self.support_ability = support_ability
        self.grenade = grenade
        self.morale = morale
        self.heal_limit = heal_limit
        self.healed_count = 0
        self.reload_time = reload_time  # 장전 시간
        self.last_attack_time = time.time() - reload_time  # 초기화 시 공격 가능하게 설정
        self.x = x  # 좌표 초기화
        self.y = y  # 좌표 초기화
        self.armor = armor
        self.recon_range = recon_range
        self.surveillance_equipment = surveillance_equipment
        self.is_ship = is_ship  # 함대 여부 체크
        
        # 통신병에게만 위치를 기록하는 속성 추가
        self.reported_positions = [] if self.can_transmit else None

    def can_attack(self):
        """현재 시점에서 공격이 가능한지 확인하는 메서드"""
        return time.time() - self.last_attack_time >= self.reload_time

    def attack_enemy(self, enemy):
        if self.can_attack():
            enemy.health -= max(1, self.attack_power - enemy.defense)
            self.last_attack_time = time.time()  # 공격 후 시간 업데이트

    def heal(self, ally):
        """의무병이 아군을 치료하는 메서드"""
        if self.healed_count < self.heal_limit:
            ally.health += 15
            self.healed_count += 1

    def update_position(self, new_x, new_y):
        """유닛의 위치 업데이트 메서드"""
        self.x = new_x
        self.y = new_y

    def can_call_airstrike(self):
        """포격 지원 가능 여부를 반환하는 메서드"""
        return True  # 기본적으로 모든 유닛이 호출할 수 없도록 설정

    def call_airstrike(self, target_x, target_y):
        """포격을 호출하는 메서드"""
        if self.can_call_airstrike():
            return {"x": target_x, "y": target_y, "damage": 100, "radius": 150}
        return None

    def call_ship_attack(self, target_x, target_y):
        """함대 포격 호출"""
        if self.is_ship:  # 함대 유닛인 경우에만 포격
            return {"x": target_x, "y": target_y, "damage": 150, "radius": 200}
        return None

# 특정 유닛 종류들 (저격병, 대전차, 드론, 의무병 등)
def create_team():
    team = []
    
    # 일반병사 50명 생성
    for _ in range(50):
        health = random.randint(85, 95)
        attack = random.randint(12, 14)
        defense = random.randint(6, 8)
        range_val = random.randint(40, 42)
        speed = random.uniform(0.9, 1.1)
        soldier = Unit("일반병사", health, attack, defense, range_val, speed, grenade=True, reload_time=1)
        team.append(soldier)
    
    # 통신병사 2명 생성
    for _ in range(2):
        health = random.randint(85, 95)
        attack = random.randint(12, 14)
        defense = random.randint(6, 8)
        range_val = random.randint(40, 42)
        speed = random.uniform(0.9, 1.1)
        soldier = Unit("통신병사", health, attack, defense, range_val, speed, vision=100, can_transmit=True, reload_time=1.5)
        team.append(soldier)
    
    # 저격병사 2명 생성
    for _ in range(2):
        soldier = Unit("저격병사", health=85, attack=50, defense=10, range=200, speed=0.6, vision=70, reload_time=2)
        team.append(soldier)

    # 대전차 3대, 드론 1대, 의무병사 1명, 함대 1대 추가
    for _ in range(3):
        team.append(Unit("대전차", health=200, attack=30, defense=20, range=50, speed=0.5, vision=40, attack_power=50, reload_time=5))
    team.append(Unit("드론", health=30, attack=0, defense=5, range=100, speed=2.0, vision=100, view_angle=360, can_transmit=True))
    team.append(Unit("의무병사", health=100, attack=10, defense=10, range=30, speed=1.0, heal_limit=5, reload_time=1))
    team.append(Unit("함대", health=500, attack=100, defense=50, range=200, speed=0, vision=100, is_ship=True))

    return team  # 팀 반환

def save_teams(filename):
    team1 = create_team()
    team2 = create_team()
    teams = {"Team1": team1, "Team2": team2}
    
    with open(filename, 'wb') as file:
        pickle.dump(teams, file)
    
    print(f"{filename} 파일에 두 팀의 유닛 정보가 저장되었습니다.")

if __name__ == "__main__":
    save_teams("unit.pkl")
