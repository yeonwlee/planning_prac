import os

# 루트 디렉토리
ROOT_DIR = os.path.dirname('./main.py')

# Data 디렉토리
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# ./data/audio
AUDIO_DIR = os.path.join(DATA_DIR, 'audio')

# 로그 파일 저장 경로 설정
# ./logs
LOG_DIR = os.path.join(ROOT_DIR, 'logs')


# 디렉토리 생성
os.makedirs(DATA_DIR, mode=0o777, exist_ok=True)
os.makedirs(AUDIO_DIR, mode=0o777, exist_ok=True)
os.makedirs(LOG_DIR, mode=0o777, exist_ok=True)