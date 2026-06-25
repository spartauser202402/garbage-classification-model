###papper 증강 오류로 인하여 papper만 증강시키는 코드 작성
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import os

# 증강 설정
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# paper 폴더만 처리
source_folder = "dataset/paper"
save_folder = "augmented/paper"

os.makedirs(save_folder, exist_ok=True)

print("paper 증강 시작")

# 사진 불러오기
for img_name in os.listdir(source_folder):

    # jpg, jpeg, png 파일만 처리
    if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    try:
        img_path = os.path.join(source_folder, img_name)

        print(f"처리중: {img_name}")

        img = image.load_img(img_path)

        x = image.img_to_array(img)

        x = x.reshape((1,) + x.shape)

        count = 0

        # 사진 2개 생성
        for batch in datagen.flow(
            x,
            batch_size=1,
            save_to_dir=save_folder,
            save_prefix="aug",
            save_format="jpg"
        ):

            count += 1

            if count >= 2:
                break

    except Exception as e:
        print(f"오류 발생: {img_name}")
        print(e)

print("paper 증강 완료!")
