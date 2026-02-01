"""
pH 예측 모듈
이미지를 입력받아 pH 값과 신뢰도를 예측합니다.
"""
import torch
import torch.nn as nn
import numpy as np
import logging
from src.model_loader import get_model, get_ph_classes, get_ph_values
from config.settings import PH_CLASSES, PH_VALUES

logger = logging.getLogger(__name__)
_mapping_verified = False


def predict_ph(image_tensor: torch.Tensor) -> dict:
    """
    이미지에서 pH 값을 예측합니다.
    
    Args:
        image_tensor: 전처리된 이미지 텐서 (1, 3, H, W)
        
    Returns:
        dict: {
            'ph_class': str,           # 예측된 pH 클래스 (예: 'pH_7')
            'ph_value': float,         # 예측된 pH 값 (예: 7.0)
            'confidence': float,        # 최고 클래스의 신뢰도 (0~1)
            'all_probabilities': dict,  # 모든 클래스의 확률
            'top2_weighted_ph': float   # Top-2 가중 평균 pH 값
        }
    """
    model = get_model()
    ph_classes = get_ph_classes()
    ph_values = get_ph_values()
    
    # 디바이스 결정
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # 모델 추론
    model.eval()
    with torch.no_grad():
        image_tensor = image_tensor.to(device)
        logits = model(image_tensor)
        
        # Softmax로 확률 변환
        softmax = nn.Softmax(dim=1)
        probabilities = softmax(logits).cpu().numpy()[0]
    
    # 최고 확률 클래스
    predicted_idx = int(np.argmax(probabilities))
    predicted_class = ph_classes[predicted_idx]
    predicted_ph = ph_values[predicted_idx]
    confidence = float(probabilities[predicted_idx])
    
    # 매핑 검증 로그 (1회만 출력)
    global _mapping_verified
    if not _mapping_verified:
        logger.info(f"PH mapping verification - predicted_idx={predicted_idx}, PH_CLASSES[{predicted_idx}]={PH_CLASSES[predicted_idx]}, PH_VALUES[{predicted_idx}]={PH_VALUES[predicted_idx]}")
        _mapping_verified = True
    
    # 모든 클래스의 확률 딕셔너리
    all_probs = {
        ph_classes[i]: float(probabilities[i])
        for i in range(len(ph_classes))
    }
    
    # Top-2 가중 평균 pH 계산
    top2_indices = np.argsort(probabilities)[-2:][::-1]
    i1, i2 = top2_indices[0], top2_indices[1]
    p1, p2 = probabilities[i1], probabilities[i2]
    ph1, ph2 = ph_values[i1], ph_values[i2]
    top2_weighted_ph = float((p1 * ph1 + p2 * ph2) / (p1 + p2 + 1e-12))
    
    return {
        "ph_class": predicted_class,
        "ph_value": predicted_ph,
        "confidence": confidence,
        "all_probabilities": all_probs,
        "top2_weighted_ph": top2_weighted_ph
    }
