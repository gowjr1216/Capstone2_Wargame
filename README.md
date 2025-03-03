1. 지형 및 유닛 생성
simulate > land 폴더에서 python land.py
-> land.pkl 생성 (지형)
simulate > unit 폴더에서 python unit.py
-> unit.pkl 생성 (유닛)

[지형 및 유닛 확인] simulate > dp 폴더
지형 : python dland.py
유닛 : python dunit.py


2. 전투모델 생성 (최적의 행동 학습)
Anaconda prompt에서 conda activate rl_env로 가상환경 접속하기
그 후, simulate > module 폴더의 python battle_module.py로
-> battle_module.zip 생성


3. 전투데이터 생성 (1000번의 전투 데이터)
simulate > module 폴더의 python data.py로
-> data.pkl 생성
// data.py와 이 파일로 생성된 파일 module로 이동할 예정


4. 모델학습 및 예측모델 저장 (예측모델)
simulate > module 폴더의 python pred_module.py로
-> pred_module.zip 생성


5. 지형, 유닛, 전투모델, 예측모델을 활용해 실전투 시뮬레이션
simulate > battle 폴더의 mainfield.py로
시뮬레이션 실행
