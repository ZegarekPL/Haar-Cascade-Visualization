import os
import cv2
import shutil

images_dir = '/home/wiktor/Downloads/WIDER_train/images'
positive_dir = '/home/wiktor/Downloads/WIDER_train/positive'
negative_dir = '/home/wiktor/Downloads/WIDER_train/negative'

os.makedirs(positive_dir, exist_ok=True)
os.makedirs(negative_dir, exist_ok=True)

cascade_path = '/home/wiktor/Documents/Git/Haar-Cascade-Visualization/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

for root, dirs, files in os.walk(images_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(root, file)

            img = cv2.imread(file_path)
            if img is None:
                print(f"Nie można otworzyć {file_path}")
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) > 0:
                dest_path = os.path.join(positive_dir, file)
            else:
                dest_path = os.path.join(negative_dir, file)

            shutil.copy2(file_path, dest_path)
            print(f"Skopiowano {file} do {'positive' if len(faces) > 0 else 'negative'}")

print("✅ Zakończono segregację zdjęć!")
