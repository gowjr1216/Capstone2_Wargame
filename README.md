# 프로젝트 이름

## 개요
이 프로젝트는 지형 생성, 유닛 생성, 전투 모델 학습 및 시뮬레이션을 포함한 전투 시뮬레이션 시스템입니다.

## 사용 기술
- Python
- Anaconda

## 설치 방법
필요한 패키지를 설치합니다. Anaconda 환경을 설정하고 필요한 패키지를 설치하세요.

## 지형 및 유닛 생성
### 1.1 지형 생성
```bash
cd simulate/land
python land.py
# land.pkl 파일 생성 (지형 데이터 저장)
```

### 1.2 유닛 생성
```bash
cd simulate/unit
python unit.py
# unit.pkl 파일 생성 (유닛 데이터 저장)
```

### 1.3 지형 및 유닛 데이터 확인
#### 지형 확인
```bash
cd simulate/dp
python dland.py
```

#### 유닛 확인
```bash
cd simulate/dp
python dunit.py
```

## 2. 전투모델 생성 (최적의 행동 학습)
Anaconda Prompt에서 다음 명령어를 실행하여 가상환경을 활성화합니다.
```bash
conda activate rl_env
```
이후, 전투모델을 생성합니다.
```bash
cd simulate/module
python battle_module.py
# battle_module.zip 파일 생성
```

## 3. 전투데이터 생성 (1000번의 전투 데이터 수집)
```bash
cd simulate/module
python data.py
# data.pkl 파일 생성
# 생성된 data.pkl 파일을 module 폴더로 이동 예정
```

## 4. 모델 학습 및 예측모델 저장
```bash
cd simulate/module
python pred_module.py
# pred_module.zip 파일 생성 (예측 모델 저장)
```

## 5. 실전투 시뮬레이션 실행
```bash
cd simulate/battle
python mainfield.py
# 지형, 유닛, 전투모델, 예측모델을 활용하여 실전투 시뮬레이션 실행
```
