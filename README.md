# 🗑️ AI 분리수거 도우미 (시각장애인을 위한 분리수거 서비스)

시각장애인이 쓰레기를 카메라에 비추거나 이미지를 업로드하면, AI가 종류를 분류하여 **음성으로 분리수거 방법을 안내**하는 서비스입니다.

> 본 프로젝트는 [vatsalparikh07/garbage-classification-model](https://github.com/vatsalparikh07/garbage-classification-model)을 **Fork**하여 개발되었습니다.

<br>

## 📌 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 목표 | 시각장애인을 위한 음성 안내 분리수거 서비스 |
| 분류 클래스 | 캔(can), 종이(paper), 플라스틱(plastic) |
| 모델 | MobileNetV2 (Transfer Learning / 파인튜닝) |
| 음성 안내 | pyttsx3 (오프라인 한국어 TTS) |
| UI | Streamlit (카메라 촬영 / 파일 업로드) |

<br>

## 🧠 모델 정보

- **베이스 모델**: MobileNetV2 (ImageNet 사전학습)
- **학습 방식**: Transfer Learning (특징 추출부 고정 후 출력층 파인튜닝)
- **데이터셋**: 캔 / 종이 / 플라스틱 총 1,576장 (학습 1,261장 / 검증 315장)
- **데이터 증강**: RandomFlip, RandomRotation, RandomZoom
- **학습 결과**: Train Accuracy 약 93.3%, Validation Accuracy 약 76.2%

<br>

## 🛠️ 기술 스택

- Python 3.11
- TensorFlow 2.20.0 / Keras 3.13.2
- Streamlit (웹 UI + 카메라 입력)
- pyttsx3 (오프라인 음성 안내)
- OpenCV, Pillow, NumPy

<br>

## 📂 프로젝트 구조

```
garbage-classification-model/
├── app.py                                       # Streamlit 메인 앱 (분류 + 음성 안내 + 카메라)
├── train.ipynb                                  # MobileNetV2 모델 학습 코드 (Google Colab)
├── augment.py                                   # 데이터 증강 코드
├── augment_papper.py                            # 종이 클래스 추가 증강 코드
├── cofusion_matrix.py                           # 모델 성능 평가 (혼동 행렬)
├── more_accuracy.py                             # 정확도 개선 실험 코드
├── garbage_classification_model_inception.keras # 학습된 모델 (별도 다운로드)
├── README.md
└── .gitignore
```

> ⚠️ 모델 파일(`garbage_classification_model_inception.keras`)은 용량 문제로 GitHub에 포함되지 않습니다. Google Drive에서 다운로드 후 프로젝트 루트에 위치시켜 주세요.

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
pip install tensorflow==2.20.0 streamlit pillow opencv-python pyttsx3
```

### 3. 모델 파일 준비
학습된 모델 파일을 Google Drive에서 다운로드하여 프로젝트 루트에 위치시킵니다.
```
garbage-classification-model/
└── garbage_classification_model_inception.keras  ← 여기에 위치
```

### 4. 앱 실행
```bash
streamlit run app.py
```

### 5. 사용 방법
앱 실행 후 두 가지 입력 방식 중 선택할 수 있습니다.

- **📷 카메라 촬영**: 쓰레기를 카메라에 비추고 촬영 → 분류 결과 및 음성 안내
- **📁 파일 업로드**: jpg, jpeg, png, mp4 형식 업로드 → 분류 결과 및 음성 안내

분류가 완료되면 결과(예: 캔), 신뢰도, 분리배출 방법이 화면에 표시되고, 동시에 **음성으로 안내**됩니다.

<br>

## 🗂️ 데이터셋

데이터는 Google Drive에서 관리되며, 클래스별 폴더 구조로 구성되어 있습니다.

📁 **[Google Drive 데이터셋 링크](https://drive.google.com/drive/folders/1Wa79cbpFMvh9enzp1iVO5G6kkXUoYxDF?usp=sharing)**

```
dataset/
├── can/      # 캔 이미지
├── paper/    # 종이 이미지
└── plastic/  # 플라스틱 이미지
```

> 원본 이미지(.heic, .webp)는 학습 전 .jpg로 변환하여 사용했습니다.

<br>

## 👥 팀원 역할 분담

| 팀원 | Branch | 담당 |
|------|--------|------|
| 강채린 | `feature/tts` | 음성 안내(TTS) + 카메라 입력 + 앱 통합 / main 브랜치 관리 |
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

각 팀원이 개별 브랜치에서 작업 후, Pull Request를 통해 코드 리뷰(Approve)를 거쳐 `main` 브랜치로 병합하였습니다.

<br>

## 📝 향후 개선 방향

- 실시간 영상 스트리밍 기반 자동 분류 (현재는 단발성 촬영 방식)
- 분류 클래스 확장 (유리, 비닐 등)
- 데이터 추가 수집 및 증강을 통한 검증 정확도 향상