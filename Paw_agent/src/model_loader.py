"""
EfficientNet 모델 로더
싱글톤 패턴으로 모델을 한 번만 로드하여 메모리 효율성을 높입니다.
"""
import torch
import torch.nn as nn
import logging
from torchvision import models
from pathlib import Path
from config.settings import MODEL_PATH, NUM_CLASSES, PH_CLASSES

logger = logging.getLogger(__name__)

_model_instance = None


def get_model():
    """
    EfficientNet 모델을 싱글톤으로 반환합니다.
    
    Returns:
        torch.nn.Module: 로드된 EfficientNet 모델
    """
    global _model_instance
    
    if _model_instance is None:
        # 디바이스 결정 (CUDA 사용 가능 여부 확인)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        logger.info(f"Loading model from: {MODEL_PATH}")
        
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
        
        # 체크포인트 로드
        ckpt = torch.load(MODEL_PATH, map_location=device)
        logger.info(f"Loaded checkpoint - Backbone: {ckpt.get('backbone', 'efficientnet_v2_s')}, Epoch: {ckpt.get('epoch', 'unknown')}")
        
        # 모델 구조 재구성
        model = models.efficientnet_v2_s(weights=None)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, NUM_CLASSES)
        
        # 가중치 로드
        model.load_state_dict(ckpt["model_state"])
        model = model.to(device)
        model.eval()
        
        _model_instance = model
        logger.info(f"Model loaded successfully on {device}")
    
    return _model_instance


def get_ph_classes():
    """
    pH 클래스 목록을 반환합니다.
    
    Returns:
        list: pH 클래스 이름 리스트
    """
    return PH_CLASSES.copy()


def get_ph_values():
    """
    각 클래스에 해당하는 실제 pH 값을 반환합니다.
    
    Returns:
        list: pH 값 리스트 [10.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    """
    return [10.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
