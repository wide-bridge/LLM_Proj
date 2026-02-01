"""
유틸리티 헬퍼 함수
"""
from pathlib import Path
import hashlib
import os


def ensure_dir(directory: Path):
    """디렉토리가 없으면 생성"""
    directory.mkdir(parents=True, exist_ok=True)


def get_file_hash(file_path: str) -> str:
    """파일의 MD5 해시값 반환"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def is_valid_image(file_path: str) -> bool:
    """이미지 파일인지 확인"""
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    return Path(file_path).suffix.lower() in valid_extensions
