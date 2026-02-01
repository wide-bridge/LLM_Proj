"""
FastAPI 메인 애플리케이션
챗봇 서비스의 진입점입니다.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from app.api.routes import router
from config.settings import API_TITLE, API_VERSION

# FastAPI 앱 생성
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="강아지 오줌 pH 분석 및 건강 관리 조언 챗봇"
)

# API 라우터 등록
app.include_router(router)

# 정적 파일 서빙
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 템플릿 디렉토리
templates_dir = Path(__file__).parent.parent / "templates"


@app.get("/")
async def root():
    """메인 페이지"""
    index_path = templates_dir / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {
        "message": "강아지 오줌 pH 분석 챗봇 API",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    print("=" * 50)
    print(f"{API_TITLE} v{API_VERSION}")
    print("=" * 50)
    print("서비스가 시작되었습니다.")
    print("API 문서: http://localhost:8000/docs")
    print("=" * 50)
    
    # 모델 사전 로드 (선택사항 - 첫 요청 시 로드되지만 사전 로드 가능)
    try:
        from src.model_loader import get_model
        get_model()
        print("✓ 모델이 사전 로드되었습니다.")
    except Exception as e:
        print(f"⚠ 모델 사전 로드 실패: {e}")
        print("  (첫 요청 시 자동으로 로드됩니다.)")
