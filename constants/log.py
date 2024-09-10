import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from constants.path_config import LOG_DIR


# 로그 파일 설정
log_file_path = LOG_DIR
os.makedirs(name=log_file_path, mode=0o777, exist_ok=True)

# 시간별로 로그 파일을 분류하는 핸들러 설정 (1시간마다 새 파일 생성)
time_rotating_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_file_path, 'application.log'),
    when='H',   # 'H'는 매 시간마다 롤오버 (다른 옵션: 'S', 'M', 'D', 'midnight', 'W0'-'W6')
    interval=1, # 1 시간 간격
    backupCount=24,  # 최대 24개의 로그 파일 보관
    encoding='utf-8'
)
time_rotating_handler.setLevel(logging.DEBUG)  # 모든 로그 레벨을 기록

# 로그 형식 설정
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
time_rotating_handler.setFormatter(formatter)
time_rotating_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"


# 에러 이상의 로그만 기록하는 핸들러 설정
error_handler = TimedRotatingFileHandler(
    filename=os.path.join(log_file_path, 'error.log'),
    when='H',
    interval=1,
    backupCount=24,
    encoding='utf-8'
)
error_handler.setLevel(logging.ERROR)  # ERROR 레벨 이상만 기록
error_handler.setFormatter(formatter)
error_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"

# 루트 로거 설정
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(time_rotating_handler)
root_logger.addHandler(error_handler)