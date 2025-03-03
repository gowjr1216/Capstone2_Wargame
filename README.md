# 프로젝트 이름

## 개요
이 프로젝트는 지형 생성, 유닛 생성, 전투 모델 학습 및 시뮬레이션을 포함한 전투 시뮬레이션 시스템입니다.

## 사용 기술
- Python
- Anaconda

## 설치 방법
1. 필요한 패키지를 설치합니다. Anaconda 환경을 설정하고 필요한 패키지를 설치하세요.

## 지형 및 유닛 생성
1. **지형 생성**:
   - `simulate > land` 폴더에서 다음 명령어 실행:
     ```bash
     python land.py
     ```
   - `land.pkl` 파일이 생성됩니다.

2. **유닛 생성**:
   - `simulate > unit` 폴더에서 다음 명령어 실행:
     ```bash
     python unit.py
     ```
   - `unit.pkl` 파일이 생성됩니다.

3. **지형 및 유닛 확인**:
   - `simulate > dp` 폴더에서 지형 확인:
     ```bash
     python dland.py
     ```
   - 유닛 확인:
     ```bash
     python dunit.py
     ```

## 전투모델 생성 (최적의 행동 학습)
1. Anaconda Prompt에서 가상환경에 접속합니다:
   ```bash
   conda activate rl_env
