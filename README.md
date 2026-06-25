# 🗑️ AI 분리수거 도우미 (시각장애인을 위한 분리수거 서비스)

시각장애인이 쓰레기 이미지를 업로드하면, AI가 종류를 분류하여 **음성으로 분리수거 방법을 안내**하는 서비스입니다.

> 본 프로젝트는 [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model)을 **Fork**하여 개발되었습니다.

<br>

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 목표 | 시각장애인을 위한 음성 안내 분리수거 서비스 |
| 분류 클래스 | 캔(can), 종이(paper), 플라스틱(plastic) |
| 모델 | MobileNetV2 (Transfer Learning / 파인튜닝) |
| 음성 안내 | gTTS (한국어 TTS) |
| UI | Streamlit |

<br>

## 🧠 모델 정보

- **베이스 모델**: MobileNetV2 (ImageNet 사전학습)
- **학습 방식**: Transfer Learning (마지막 분류 레이어 교체 후 파인튜닝)
- **데이터셋**: 캔 / 종이 / 플라스틱 각 500장 (총 1,500장)
- **데이터 증강**: RandomFlip, RandomRotation, RandomZoom
- **학습 결과**: Train Accuracy 약 93%, Validation Accuracy 약 77%

<br>

## 🛠️ 기술 스택

- Python 3.11
- TensorFlow 2.20.0 / Keras 3.13.2
- Streamlit
- gTTS (Google Text-to-Speech)
- OpenCV, Pillow, NumPy

<br>

## 📂 프로젝트 구조

```
garbage-classification-model/
├── app.py                      # Streamlit 메인 앱 (분류 + 음성 안내)
├── train.ipynb                 # MobileNetV2 모델 학습 코드 (Google Colab)
├── augment.py                  # 데이터 증강 코드
├── augment_papper.py           # 종이 클래스 추가 증강 코드
├── cofusion_matrix.py          # 모델 성능 평가 (혼동 행렬)
├── more_accuracy.py            # 정확도 개선 실험 코드
├── garbage_classification_model_inception.keras  # 학습된 모델 (별도 다운로드)
├── README.md
└── .gitignore
```

> ⚠️ 모델 파일(`garbage_classification_model_inception.keras`)은 용량 문제로 GitHub에 포함되지 않습니다.
> 아래 Google Drive 링크에서 다운로드 후 프로젝트 루트에 위치시켜 주세요.

<br>

## ▶️ 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/spartauser202402/garbage-classification-model.git
cd garbage-classification-model
```

### 2. 가상환경 생성 및 라이브러리 설치
```bash
conda create -n recycling python=3.11
conda activate recycling
pip install tensorflow==2.20.0 streamlit pillow opencv-python gtts
```

### 3. 모델 파일 준비

학습된 모델 파일을 아래 링크에서 다운로드하여 프로젝트 루트에 위치시킵니다.

```
garbage-classification-model/
└── garbage_classification_model_inception.keras  ← 여기에 위치
```

### 4. 앱 실행
```bash
streamlit run app.py
```

### 5. 사용 방법
- **📁 이미지 업로드**: jpg, jpeg, png 형식의 쓰레기 이미지 업로드 → 분류 결과 및 음성 안내
- **🎬 영상 업로드**: mp4 형식의 영상 업로드 → 프레임 추출 후 분류 결과 및 음성 안내

<br>

## 🗂️ 데이터셋

📁 [Google Drive 데이터셋 링크](https://drive.google.com/drive/folders/1VMDWuIymYWD2PcoS117_RasehpnIZBIC?usp=sharing)

데이터는 Google Drive에서 관리되며, 클래스별 폴더 구조로 구성되어 있습니다.

```
dataset/
├── can/      # 캔 이미지 (500장)
├── paper/    # 종이 이미지 (500장)
└── plastic/  # 플라스틱 이미지 (500장)
```

> 원본 이미지(.heic, .webp)는 학습 전 .jpg로 변환하여 사용했습니다.

<br>

## 👥 팀원 역할 분담

| 팀원 | Branch | 담당 |
|------|--------|------|
| 강채린 | `feature/tts` | 음성 안내(TTS) 기능 + 앱 통합 |
| 이현지 | `feature/finetune` | MobileNetV2 모델 학습 / 파인튜닝 |
| 안유빈 | `feature/preprocessing` | 데이터 전처리 / 증강 |

<br>

## 🔄 협업 방식 (Git Workflow)

```
main (베이스)
   │
   ├── feature/tts           → PR → merge
   ├── feature/finetune      → PR → merge
   └── feature/preprocessing → PR → merge
```

각 팀원이 개별 브랜치에서 작업 후, Pull Request를 통해 코드 리뷰 및 `main` 브랜치로 병합하였습니다.

<br>

## 📝 향후 개선 방향

- 실시간 웹캠 기반 자동 분류 기능 추가
- 분류 클래스 확장 (유리, 비닐 등)
- 데이터 추가 수집 및 증강을 통한 검증 정확도 향상
- 오프라인 TTS(pyttsx3) 적용으로 네트워크 의존성 제거
