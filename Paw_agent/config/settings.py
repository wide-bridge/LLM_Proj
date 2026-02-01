"""
설정 관리 모듈
외부 경로의 .env 파일에서 환경 변수를 로드합니다.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일 로드
ENV_FILE = os.getenv("ENV_FILE")
if ENV_FILE:
    env_path = Path(ENV_FILE)
    if not env_path.exists():
        raise FileNotFoundError(f"ENV_FILE specified but not found: {env_path}")
    load_dotenv(env_path)
    logger.info(f"Loaded .env from: {env_path}")
else:
    load_dotenv()
    logger.info("Loaded .env from default locations")

# OpenAI API 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# 모델 설정
# .env의 MODEL_PATH가 있으면 우선 사용, 없으면 fallback
env_model_path = os.getenv("MODEL_PATH")
if env_model_path:
    MODEL_PATH = Path(env_model_path).resolve()
    logger.info(f"Using MODEL_PATH from .env: {MODEL_PATH}")
else:
    MODEL_PATH = (Path(__file__).parent.parent / "models" / "cnn" / "best_efficientnet_ph.pt").resolve()
    logger.info(f"Using default MODEL_PATH: {MODEL_PATH}")

NUM_CLASSES = 7
IMG_SIZE = 224  # EfficientNet 입력 크기

# 클래스 순서 (모델 학습 시 사용된 순서와 동일해야 함)
# ImageFolder는 알파벳 순으로 정렬하므로: pH_10, pH_4, pH_5, pH_6, pH_7, pH_8, pH_9
PH_CLASSES = ["pH_10", "pH_4", "pH_5", "pH_6", "pH_7", "pH_8", "pH_9"]
PH_VALUES = [10.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]  # 각 클래스의 실제 pH 값

# 업로드 설정
UPLOAD_DIR = Path(__file__).parent.parent / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# API 설정
API_TITLE = "강아지 오줌 pH 분석 챗봇"
API_VERSION = "1.0.0"
