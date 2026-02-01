// DOM 요소
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewArea = document.getElementById('previewArea');
const previewImage = document.getElementById('previewImage');
const removeBtn = document.getElementById('removeBtn');
const resultSection = document.getElementById('resultSection');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');

// 업로드 영역 클릭 이벤트
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// 파일 선택 이벤트
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
});

// 드래그 앤 드롭 이벤트
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#764ba2';
});

uploadArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '#667eea';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFile(file);
    } else {
        showError('이미지 파일만 업로드 가능합니다.');
    }
});

// 파일 처리 함수
function handleFile(file) {
    // 파일 크기 검사 (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('파일 크기는 10MB 이하여야 합니다.');
        return;
    }

    // 이미지 미리보기
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadArea.style.display = 'none';
        previewArea.style.display = 'block';
        
        // 예측 요청
        predictImage(file);
    };
    reader.readAsDataURL(file);
}

// 이미지 제거 버튼
removeBtn.addEventListener('click', () => {
    fileInput.value = '';
    uploadArea.style.display = 'block';
    previewArea.style.display = 'none';
    resultSection.style.display = 'none';
    hideError();
});

// 예측 API 호출
async function predictImage(file) {
    showLoading();
    hideError();
    resultSection.style.display = 'none';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '예측 중 오류가 발생했습니다.');
        }

        const data = await response.json();
        displayResults(data);

    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

// 결과 표시
function displayResults(data) {
    // pH 값 표시
    document.getElementById('phValue').textContent = data.ph_value.toFixed(1);
    
    // 신뢰도 표시
    const confidencePercent = (data.confidence * 100).toFixed(1);
    document.getElementById('confidenceFill').style.width = `${data.confidence * 100}%`;
    document.getElementById('confidenceText').textContent = `${confidencePercent}%`;

    // 확률 바 차트 표시
    displayProbabilities(data.all_probabilities, data.ph_class);

    // 건강 조언 표시
    displayAdvice(data.health_advice);

    resultSection.style.display = 'block';
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// 확률 바 차트 표시
function displayProbabilities(probabilities, predictedClass) {
    const container = document.getElementById('probabilities');
    container.innerHTML = '';

    // 확률 순으로 정렬
    const sorted = Object.entries(probabilities)
        .sort((a, b) => b[1] - a[1]);

    sorted.forEach(([phClass, prob]) => {
        const item = document.createElement('div');
        item.className = 'prob-item';
        
        const isPredicted = phClass === predictedClass;
        const labelStyle = isPredicted ? 'font-weight: bold; color: #667eea;' : '';
        
        item.innerHTML = `
            <span class="prob-label" style="${labelStyle}">${phClass}</span>
            <div class="prob-bar-container">
                <div class="prob-bar" style="width: ${prob * 100}%"></div>
            </div>
            <span class="prob-value">${(prob * 100).toFixed(1)}%</span>
        `;
        
        container.appendChild(item);
    });
}

// 건강 조언 표시
function displayAdvice(advice) {
    const content = document.getElementById('adviceContent');
    
    // 마크다운 스타일을 HTML로 변환 (간단한 버전)
    let html = advice
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>')
        .replace(/^### (.*)$/gm, '<h3>$1</h3>')
        .replace(/^## (.*)$/gm, '<h3>$1</h3>')
        .replace(/^(\d+\.\s.*)$/gm, '<p>$1</p>')
        .replace(/^-\s(.*)$/gm, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');
    
    content.innerHTML = html;
}

// 로딩 표시/숨김
function showLoading() {
    loading.style.display = 'block';
}

function hideLoading() {
    loading.style.display = 'none';
}

// 에러 표시/숨김
function showError(message) {
    errorMessage.textContent = `❌ ${message}`;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}
