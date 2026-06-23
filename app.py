import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
import os
from gtts import gTTS
import base64

# 학습된 모델 불러오기
model = tf.keras.models.load_model("garbage_classification_model_inception.keras")

# 이미지 크기
img_height = 384
img_width = 512

# 클래스 정의
waste_categories = ['can', 'paper', 'plastic']

# 한국어 변환
label_ko = {
    'can': '캔',
    'paper': '종이',
    'plastic': '플라스틱'
}

# 분리수거 안내
disposal_info = {
    'can': "캔은 내용물을 비우고 찌그러뜨려 배출하세요.",
    'paper': "종이는 깨끗한 상태로 묶어서 배출하세요.",
    'plastic': "플라스틱은 내용물을 비우고 라벨을 제거한 후 배출하세요."
}

# TTS 음성 출력 함수
def speak(text):
    tts = gTTS(text=text, lang='ko')
    tts.save("result.mp3")
    with open("result.mp3", "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{audio_b64}"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

# 이미지로 분류하는 함수
def predict_from_image(image):
    img = image.resize((img_width, img_height))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)
    confidence = np.max(prediction)
    predicted_category = waste_categories[predicted_index]
    return predicted_category, confidence

# 영상으로 분류하는 함수
def predict_from_video(video_bytes):
    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)
    cap = cv2.VideoCapture("temp_video.mp4")
    for _ in range(20):
        ret, _ = cap.read()
    ret, frame = cap.read()
    if ret:
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return predict_from_image(pil_image), frame
    else:
        raise RuntimeError("영상 처리 실패")

# Streamlit 앱
def main():
    st.title("🗑️ AI 분리수거 도우미")
    st.markdown("이미지 또는 영상을 업로드하면 분리수거 방법을 음성으로 안내해드립니다.")

    uploaded_file = st.file_uploader(
        "이미지 또는 영상 업로드",
        type=["jpg", "jpeg", "png", "mp4"]
    )

    if uploaded_file is not None:
        if uploaded_file.type.startswith('image'):
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)
            predicted_category, confidence = predict_from_image(image)

        elif uploaded_file.type.startswith('video'):
            try:
                (predicted_category, confidence), frame = predict_from_video(uploaded_file.read())
                st.video(uploaded_file)
            except RuntimeError as e:
                st.error(str(e))
                return
        else:
            st.error("jpg, jpeg, png, mp4 형식만 지원합니다.")
            return

        # 결과 출력
        label = label_ko.get(predicted_category, predicted_category)
        st.subheader(f"분류 결과: {label}")
        st.write(f"신뢰도: {confidence*100:.1f}%")

        # 분리수거 안내
        st.subheader("분리수거 방법:")
        st.write(disposal_info.get(predicted_category, "정보 없음"))

        # 🔊 TTS 음성 출력
        message = f"{label}입니다. 신뢰도 {confidence*100:.0f}퍼센트. {disposal_info.get(predicted_category, '')}"
        speak(message)

if __name__ == "__main__":
    main()