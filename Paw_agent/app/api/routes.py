"""
FastAPI 라우트 정의
이미지 업로드 및 pH 예측 API 엔드포인트입니다.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import torch
from pathlib import Path
import shutil

from app.api.schemas import PredictionResponse, ErrorResponse
from src.image_processor import preprocess_image_from_bytes
from src.predictor import predict_ph
from src.health_advisor import get_health_advice
from config.settings import UPLOAD_DIR, MAX_UPLOAD_SIZE

router = APIRouter(prefix="/api", tags=["pH Prediction"])


@router.post("/predict", response_model=PredictionResponse)
async def predict_ph_from_image(file: UploadFile = File(...)):
    """
    이미지를 업로드하여 pH 값을 예측하고 건강 조언을 받습니다.
    
    Args:
        file: 업로드된 이미지 파일
        
    Returns:
        PredictionResponse: pH 예측 결과 및 건강 조언
    """
    # 파일 유효성 검사
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="이미지 파일만 업로드 가능합니다."
        )
    
    try:
        # 파일 읽기
        contents = await file.read()
        
        # 파일 크기 검사
        if len(contents) > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"파일 크기는 {MAX_UPLOAD_SIZE / 1024 / 1024:.1f}MB 이하여야 합니다."
            )
        
        # 이미지 전처리
        image_tensor = preprocess_image_from_bytes(contents)
        
        # pH 예측
        prediction = predict_ph(image_tensor)
        
        # 건강 조언 생성
        health_advice = get_health_advice(
            ph_value=prediction["ph_value"],
            ph_class=prediction["ph_class"],
            confidence=prediction["confidence"]
        )
        
        # 응답 구성
        response = PredictionResponse(
            ph_class=prediction["ph_class"],
            ph_value=prediction["ph_value"],
            confidence=prediction["confidence"],
            all_probabilities=prediction["all_probabilities"],
            top2_weighted_ph=prediction["top2_weighted_ph"],
            health_advice=health_advice
        )
        
        return response
    
    except torch.cuda.OutOfMemoryError:
        raise HTTPException(
            status_code=500,
            detail="GPU 메모리 부족입니다. 잠시 후 다시 시도해주세요."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"예측 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """서비스 상태 확인"""
    return {"status": "healthy", "message": "pH Prediction API is running"}
