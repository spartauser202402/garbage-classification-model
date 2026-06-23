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


# 처리할 폴더들
classes = ["plastic", "can", "paper"]


for class_name in classes:

    source_folder = f"dataset/{class_name}"
    save_folder = f"augmented/{class_name}"

    os.makedirs(save_folder, exist_ok=True)

    print(class_name + " 증강 시작")


    # 사진 불러오기
    for img_name in os.listdir(source_folder):

        img_path = os.path.join(source_folder, img_name)

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


    print(class_name + " 증강 완료")


print("전체 데이터 증강 완료!")