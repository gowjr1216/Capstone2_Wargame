# dunit.py
# unit.pkl을 보여주는 코드

import pickle
import tkinter as tk
from tkinter import ttk
import sys
import os

# 경로
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'unit'))  # 'unit' 폴더 경로 추가
from unit import Unit  # Unit 모듈을 import

def display_units(filename):
    # unit.pkl 경로 설정
    unit_file_path = os.path.join(os.path.dirname(__file__), '..', 'unit', filename)  # unit.pkl 경로 설정
    
    with open(unit_file_path, 'rb') as file:
        data = pickle.load(file)
    
    root = tk.Tk()
    root.title("Teams Overview")
    root.geometry("700x500")

    # 메인 프레임 생성
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Canvas를 사용하여 스크롤 기능 추가
    canvas = tk.Canvas(main_frame)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.pack(side="left", fill="both", expand=True)

    def _on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

    # 유닛의 정보 표시 함수
    def unit_info(unit):
        return (
            f"역할: {unit.role}\n"
            f"체력: {unit.health}, 공격력: {unit.attack if unit.role != '드론' else 'N/A'}, 방어력: {unit.defense}\n"
            f"사정거리: {unit.range if unit.role != '드론' else 'N/A'}, 속도: {unit.speed}\n"
            f"시야 거리: {unit.vision}, 시야 각도: {unit.view_angle}도\n"
            f"통신 가능 여부: {'Yes' if unit.can_transmit else 'No'}\n"
            f"초기 시야 방향: {unit.view_direction}도\n"
            f"장전 시간: {getattr(unit, 'reload_time', 'N/A')}초\n"
            f"추가 공격력: {unit.attack_power if unit.role != '드론' else 'N/A'}\n"
            f"지원 가능 여부: {'Yes' if unit.support_ability else 'No'}\n"
            f"수류탄 여부: {'Yes' if unit.grenade else 'No'}\n"
            f"사기: {getattr(unit, 'morale', 'N/A')}\n"
            f"의무병 치료 제한: {getattr(unit, 'heal_limit', 'N/A')}\n"
            f"의무병 치료 횟수: {getattr(unit, 'healed_count', 'N/A')}"
        )

    # 함대 포격 정보 표시 함수
    def ship_attack_info(unit):
        if unit.is_ship:
            return (
                f"함대 포격 지원\n"
                f"공격력: {unit.attack_power}\n"
                f"범위: {unit.range}\n"
                f"속도: {unit.speed}\n"
            )
        return "이 유닛은 함대가 아닙니다."

    # 유닛 아코디언 토글 함수
    def toggle_unit_details(summary_frame):
        if not summary_frame.children_labels:
            for idx, unit in enumerate(summary_frame.unit_list):
                label = tk.Label(summary_frame, text=f"{unit.role} {idx+1} - {unit_info(unit)}", anchor="w")
                label.pack(fill="x", padx=10)
                summary_frame.children_labels.append(label)
        else:
            for label in summary_frame.children_labels:
                label.destroy()
            summary_frame.children_labels.clear()

    # 팀 프레임 구성
    def create_team_frame(team_name, team_data, col):
        team_frame = ttk.LabelFrame(scrollable_frame, text=team_name, padding="10")
        team_frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")

        # 유닛 종류별 아코디언 구성
        unit_types = {
            "일반병사": [unit for unit in team_data if unit.role == "일반병사"],
            "통신병사": [unit for unit in team_data if unit.role == "통신병사"],
            "저격병사": [unit for unit in team_data if unit.role == "저격병사"],
            "의무병사": [unit for unit in team_data if unit.role == "의무병사"]
        }

        for unit_type, units in unit_types.items():
            if units:
                summary_frame = tk.Frame(team_frame)
                summary_frame.pack(fill="x", pady=5)

                # 아코디언 버튼 생성
                summary_frame.unit_list = units
                summary_frame.children_labels = []
                unit_label = tk.Label(
                    summary_frame, text=f"{unit_type} {len(units)}명 - 클릭하여 상세 정보 보기", fg="blue", cursor="hand2"
                )
                unit_label.pack(anchor="w")
                unit_label.bind("<Button-1>", lambda e, sf=summary_frame: toggle_unit_details(sf))

        # 병사 아래 한 칸 띄우기
        tk.Label(team_frame, text=" ").pack(anchor="w")

        # 대전차, 드론, 함대 정보 추가
        special_units = {
            "대전차": [unit for unit in team_data if unit.role == "대전차"],
            "드론": [unit for unit in team_data if unit.role == "드론"]
        }

        for unit_type, units in special_units.items():
            if units:
                summary_frame = tk.Frame(team_frame)
                summary_frame.pack(fill="x", pady=5)

                # 단위 결정
                unit_count_text = f"{len(units)}대"

                # 아코디언 버튼 생성
                summary_frame.unit_list = units
                summary_frame.children_labels = []
                unit_label = tk.Label(
                    summary_frame, text=f"{unit_type} {unit_count_text} - 클릭하여 상세 정보 보기", fg="blue", cursor="hand2"
                )
                unit_label.pack(anchor="w")
                unit_label.bind("<Button-1>", lambda e, sf=summary_frame: toggle_unit_details(sf))

        # 함대(포격) 아코디언 생성
        ship_units = [unit for unit in team_data if unit.is_ship]
        for ship in ship_units:
            airstrike_frame = tk.Frame(team_frame)
            airstrike_frame.pack(fill="x", pady=5)
            airstrike_frame.children_labels = []
            airstrike_label = tk.Label(
                airstrike_frame, text="함대 1대 - 클릭하여 포격 정보 보기", fg="blue", cursor="hand2"
            )
            airstrike_label.pack(anchor="w")
            airstrike_label.bind(
                "<Button-1>",
                lambda e, frame=airstrike_frame, unit=ship: toggle_airstrike_details(frame, unit)
            )

    # 함대 포격 아코디언 토글 함수
    def toggle_airstrike_details(frame, unit):
        if not frame.children_labels:
            label = tk.Label(frame, text=ship_attack_info(unit), anchor="w")
            label.pack(fill="x", padx=10)
            frame.children_labels.append(label)
        else:
            for label in frame.children_labels:
                label.destroy()
            frame.children_labels.clear()

    # Team 1 및 Team 2 구성
    create_team_frame("Team 1", data["Team1"], col=0)
    create_team_frame("Team 2", data["Team2"], col=1)

    root.mainloop()

if __name__ == "__main__":
    display_units("unit.pkl")
