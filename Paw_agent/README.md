# 강아지 오줌 pH 분석 챗봇

EfficientNet 모델을 사용하여 강아지 오줌의 pH 값을 분석하고, OpenAI API를 통해 건강 관리 조언을 제공하는 웹 챗봇입니다.

## 주요 기능

- 🖼️ **이미지 업로드**: 강아지 오줌 이미지를 업로드하여 pH 값 분석
- 📊 **pH 분류**: 7개 클래스 (pH 4~10) 분류 및 신뢰도 표시
- 💡 **건강 조언**: OpenAI API를 통한 맞춤형 건강 관리 방법 제공
- 🎨 **직관적인 UI**: 현대적이고 사용하기 쉬운 웹 인터페이스

## 프로젝트 구조

```
Paw_agent/
├── app/                    # FastAPI 애플리케이션
│   ├── main.py            # 메인 앱
│   └── api/               # API 엔드포인트
├── src/                    # 핵심 로직
│   ├── model_loader.py   # 모델 로딩
│   ├── predictor.py      # pH 예측
│   ├── image_processor.py # 이미지 전처리
│   └── health_advisor.py  # OpenAI API 연동
├── config/                # 설정
│   └── settings.py        # 환경 변수 관리
├── templates/             # HTML 템플릿
├── static/                # 정적 파일 (CSS, JS)
├── models/                # 학습된 모델
└── datasets/              # 데이터셋
```

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일은 다음 경로에 있어야 합니다:
```
D:\PyProject\DocTalk\Derma_AI\Face_Derma_Proj\.env
```

`.env` 파일에 다음 내용이 포함되어 있어야 합니다:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 애플리케이션 실행

```bash
python run.py
```

또는 직접 uvicorn 실행:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 웹 브라우저에서 접속

```
http://localhost:8000
```

API 문서는 다음에서 확인할 수 있습니다:
```
http://localhost:8000/docs
```

## 사용 방법

1. 웹 브라우저에서 `http://localhost:8000` 접속
2. 이미지 업로드 영역에 강아지 오줌 이미지 업로드 (드래그 앤 드롭 또는 클릭)
3. 자동으로 pH 값 분석 및 건강 조언 확인

## API 엔드포인트

### POST `/api/predict`
이미지를 업로드하여 pH 값을 예측합니다.

**요청:**
- `file`: 이미지 파일 (multipart/form-data)

**응답:**
```json
{
  "ph_class": "pH_7",
  "ph_value": 7.0,
  "confidence": 0.95,
  "all_probabilities": {
    "pH_4": 0.01,
    "pH_5": 0.02,
    ...
  },
  "top2_weighted_ph": 7.1,
  "health_advice": "강아지의 오줌 pH가 정상 범위입니다..."
}
```

### GET `/api/health`
서비스 상태를 확인합니다.

## 기술 스택

- **Backend**: FastAPI, Python
- **ML Model**: PyTorch, EfficientNet V2 Small
- **AI**: OpenAI GPT-3.5 Turbo
- **Frontend**: HTML, CSS, JavaScript (Vanilla)

## 주의사항

⚠️ 이 서비스는 참고용입니다. 정확한 진단은 수의사와 상담하세요.

## 라이선스

MIT License
