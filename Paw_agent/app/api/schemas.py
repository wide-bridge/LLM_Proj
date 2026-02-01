"""
Pydantic 스키마 정의
API 요청/응답 검증을 위한 모델입니다.
"""
from pydantic import BaseModel
from typing import Dict, Optional


class PredictionResponse(BaseModel):
    """pH 예측 응답 모델"""
    ph_class: str
    ph_value: float
    confidence: float
    all_probabilities: Dict[str, float]
    top2_weighted_ph: float
    health_advice: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "ph_class": "pH_7",
                "ph_value": 7.0,
                "confidence": 0.95,
                "all_probabilities": {
                    "pH_4": 0.01,
                    "pH_5": 0.02,
                    "pH_6": 0.05,
                    "pH_7": 0.95,
                    "pH_8": 0.01,
                    "pH_9": 0.01,
                    "pH_10": 0.01
                },
                "top2_weighted_ph": 7.1,
                "health_advice": "강아지의 오줌 pH가 정상 범위입니다..."
            }
        }


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str
    detail: Optional[str] = None
