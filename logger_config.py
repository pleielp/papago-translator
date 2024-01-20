import os
import logging


# 로거 설정갋 가져오기
LOG_DIR = os.environ.get('LOG_DIR')
LOG_FILE = os.environ.get('LOG_FILE')
LOG_PATH = LOG_DIR + LOG_FILE
LOG_FORMAT = os.environ.get('LOG_FORMAT')
LOG_DATE_FORMAT = os.environ.get('LOG_DATE_FORMAT')
LOG_LEVEL = os.environ.get('LOG_LEVEL')

# 로그 폴더/파일이 없으면 생성
if not os.path.isdir(LOG_DIR):
  os.mkdir(LOG_DIR)
if not os.path.exists(LOG_FILE):
    f = open(LOG_PATH, 'a').close()
else:
    f = open(LOG_PATH,"w").close()

# 로거 생성
def get_logger(name):
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')  # 인코딩 지정
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger