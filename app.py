import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tensorflow as tf
import os

# ✅ 모델 로드
model = tf.keras.models.load_model("garbage_classification_model_inception.h5")

# ✅ 이미지 크기 (학습과 동일)
img_height = 224
img_width = 224

# ✅ 클래스 순서 (⭐ 매우 중요)
waste_categories = ['can', 'paper', 'plastic']

# ✅ 쓰레기통 색
dustbin_colors = {
    'paper': 'blue',
    'plastic': 'blue',
    'can': 'blue'
}

# ✅ 분리배출 정보
disposal_info = {
    'paper': "종이는 깨끗한 상태로 분리배출하세요.",
    'plastic': "플라스틱은 내용물을 비우고 배출하세요.",
    'can': "캔과 병은 세척 후 배출하세요."
}

# ✅ 비율 유지 + padding
def resize_with_padding(image, target_size=(224, 224)):
    image = image.copy()
    image.thumbnail(target_size)
    new_img = Image.new("RGB", target_size)
    new_img.paste(
        image,
        ((target_size[0] - image.size[0]) // 2,
         (target_size[1] - image.size[1]) // 2)
    )
    return new_img

# ✅ 이미지 예측
def predict_waste_category_from_image(image):
    img = resize_with_padding(image, (img_height, img_width))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_index = np.argmax(prediction)

    predicted_category = waste_categories[predicted_index]
    confidence = np.max(prediction)

    return predicted_category, confidence

# ✅ 영상 예측
def predict_waste_category_from_video(video_bytes):
    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture("temp_video.mp4")

    for _ in range(20):
        ret, _ = cap.read()

    ret, frame = cap.read()

    if ret:
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        result = predict_waste_category_from_image(pil_image)
        return result, frame
    else:
        raise RuntimeError("영상 처리 실패")

# ✅ 쓰레기통 이미지 경로
def get_dustbin_image_path(color):
    return os.path.join("dustbin_images", f"{color}.png")

# ✅ 메인 앱
def main():
    st.title("AI 분리수거 도우미")

    uploaded_file = st.file_uploader(
        "이미지 또는 영상 업로드", 
        type=["jpg", "jpeg", "png", "mp4"]
    )

    if uploaded_file:
        if uploaded_file.type.startswith('image'):
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드 이미지")

            predicted_category, confidence = predict_waste_category_from_image(image)

        else:
            (result, frame) = predict_waste_category_from_video(uploaded_file.read())
            predicted_category, confidence = result
            st.video(uploaded_file)

        st.subheader(f"예측 결과: {predicted_category}")
        st.write(f"신뢰도: {confidence:.2f}")

        st.subheader("분리배출 방법")
        st.write(disposal_info[predicted_category])

        color = dustbin_colors[predicted_category]
        img_path = get_dustbin_image_path(color)

        if os.path.exists(img_path):
            st.image(img_path, caption="추천 쓰레기통", width=200)

# ✅ 실행
if __name__ == "__main__":
    main()
