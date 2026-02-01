"""
강아지 건강 관리 조언 생성 모듈
OpenAI API를 사용하여 pH 값에 따른 건강 관리 방법을 제공합니다.
"""
from openai import OpenAI
from config.settings import OPENAI_API_KEY

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)


def get_health_advice(ph_value: float, ph_class: str, confidence: float) -> str:
    """
    pH 값에 따른 강아지 건강 관리 조언을 생성합니다.
    
    Args:
        ph_value: 예측된 pH 값
        ph_class: 예측된 pH 클래스 (예: 'pH_7')
        confidence: 예측 신뢰도
        
    Returns:
        str: 건강 관리 조언 텍스트
    """
    # pH 값에 따른 기본 상태 판단
    if ph_value <= 6.0:
        status = "산성 (Acidic)"
        concern = "산성 오줌은 요로 감염이나 신장 문제의 징후일 수 있습니다."
    elif ph_value >= 8.0:
        status = "알칼리성 (Alkaline)"
        concern = "알칼리성 오줌은 요로 감염이나 특정 약물의 영향일 수 있습니다."
    else:
        status = "정상 범위 (Normal)"
        concern = "정상 범위의 pH 값을 보이고 있습니다."
    
    # 프롬프트 구성
    system_prompt = """당신은 수의학 전문가입니다. 강아지의 오줌 pH 값에 따른 건강 관리 방법을 
친절하고 전문적으로 설명해주세요. 한국어로 답변해주세요."""

    user_prompt = f"""강아지의 오줌 pH 값이 {ph_value} ({ph_class})로 측정되었습니다.
예측 신뢰도는 {confidence:.1%}입니다.

현재 상태: {status}
우려사항: {concern}

이 pH 값에 따른 강아지의 건강 관리 방법을 구체적으로 알려주세요. 
다음 항목들을 포함해주세요:
1. 현재 pH 값의 의미
2. 주의해야 할 증상
3. 권장되는 관리 방법 (식이, 수분 섭취 등)
4. 수의사 상담이 필요한 경우
5. 일상적인 관리 팁

간결하고 실용적인 조언을 제공해주세요."""

    try:
        # OpenAI API 호출 (최신 SDK 사용)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4" 사용 가능
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        advice = response.choices[0].message.content.strip()
        return advice
    
    except Exception as e:
        # API 호출 실패 시 기본 조언 반환
        return get_default_advice(ph_value, status)


def get_default_advice(ph_value: float, status: str) -> str:
    """
    OpenAI API 호출 실패 시 기본 조언을 반환합니다.
    
    Args:
        ph_value: pH 값
        status: 상태 설명
        
    Returns:
        str: 기본 조언 텍스트
    """
    if ph_value <= 6.0:
        return f"""**pH {ph_value} - 산성 (Acidic)**

**의미:**
강아지의 오줌이 산성으로 측정되었습니다. 이는 정상 범위보다 낮은 값입니다.

**주의사항:**
- 요로 감염 가능성
- 신장 질환 징후
- 특정 약물의 영향

**권장 관리 방법:**
1. 충분한 수분 섭취를 유도하세요
2. 수의사와 상담하여 정확한 진단을 받으세요
3. 요로 감염 증상(자주 소변 보기, 통증 등)을 관찰하세요
4. 처방된 약물이 있다면 복용을 계속하세요

**수의사 상담 필요:**
- pH 값이 계속 낮게 유지되는 경우
- 다른 증상(식욕 부진, 무기력 등)이 동반되는 경우
- 소변 색상이나 냄새에 이상이 있는 경우"""
    
    elif ph_value >= 8.0:
        return f"""**pH {ph_value} - 알칼리성 (Alkaline)**

**의미:**
강아지의 오줌이 알칼리성으로 측정되었습니다. 이는 정상 범위보다 높은 값입니다.

**주의사항:**
- 요로 감염 가능성
- 특정 박테리아 감염
- 약물의 영향

**권장 관리 방법:**
1. 수의사와 상담하여 원인을 파악하세요
2. 충분한 수분 섭취를 유도하세요
3. 요로 감염 증상을 관찰하세요
4. 처방된 항생제가 있다면 완전히 복용하세요

**수의사 상담 필요:**
- pH 값이 계속 높게 유지되는 경우
- 소변에 피가 섞여 있거나 탁한 경우
- 배뇨 시 통증을 보이는 경우"""
    
    else:
        return f"""**pH {ph_value} - 정상 범위 (Normal)**

**의미:**
강아지의 오줌 pH가 정상 범위(6.5~7.5)에 있습니다. 건강한 상태입니다.

**일상 관리:**
1. 충분한 깨끗한 물을 제공하세요
2. 균형 잡힌 사료를 급여하세요
3. 정기적인 산책과 운동을 시켜주세요
4. 정기적인 건강 검진을 받으세요

**건강 유지 팁:**
- 매일 충분한 수분 섭취 확인
- 소변 색상과 냄새 관찰
- 배뇨 빈도와 양 확인
- 정기적인 수의사 검진 (연 1~2회)"""
