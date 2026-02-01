"""
이미지 전처리 모듈
업로드된 이미지를 모델 입력 형식으로 변환합니다.
"""
import torch
from PIL import Image
import torchvision.transforms as transforms
from config.settings import IMG_SIZE


def preprocess_image(image_path: str) -> torch.Tensor:
    """
    이미지를 모델 입력 형식으로 전처리합니다.
    
    Args:
        image_path: 이미지 파일 경로
        
    Returns:
        torch.Tensor: 전처리된 이미지 텐서 (1, 3, IMG_SIZE, IMG_SIZE)
    """
    # 이미지 로드
    image = Image.open(image_path).convert("RGB")
    
    # 전처리 파이프라인 (학습 시 사용한 것과 동일해야 함)
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],  # ImageNet 평균
            std=[0.229, 0.224, 0.225]   # ImageNet 표준편차
        )
    ])
    
    # 전처리 및 배치 차원 추가
    tensor = transform(image).unsqueeze(0)
    
    return tensor


def preprocess_image_from_bytes(image_bytes: bytes) -> torch.Tensor:
    """
    바이트 데이터에서 이미지를 로드하고 전처리합니다.
    
    Args:
        image_bytes: 이미지 바이트 데이터
        
    Returns:
        torch.Tensor: 전처리된 이미지 텐서
    """
    from io import BytesIO
    
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    tensor = transform(image).unsqueeze(0)
    
    return tensor
