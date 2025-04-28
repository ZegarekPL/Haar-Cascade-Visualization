import os
import cv2
from tqdm import tqdm

base_dir = '/home/wiktor/Downloads/WIDER_train'
positive_dir = os.path.join(base_dir, 'positive')
positives_txt = os.path.join(base_dir, 'positives.txt')
haar_cascade_path = '/home/wiktor/Documents/Git/Haar-Cascade-Visualization/haarcascade_frontalface_default.xml'

def create_positives_list():
    face_cascade = cv2.CascadeClassifier(haar_cascade_path)
    img_files = [img for img in os.listdir(positive_dir) if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
    with open(positives_txt, 'w') as f:
        for img_name in tqdm(img_files, desc="Tworzenie positives.txt"):
            img_path = os.path.join(positive_dir, img_name)
            img = cv2.imread(img_path)
            if img is None:
                continue
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                continue
            x, y, w, h = faces[0]  # pierwsza wykryta twarz
            f.write(f"{img_path} 1 {x} {y} {w} {h}\n")
    print(f"[+] Stworzono positives.txt ({positives_txt})")

if __name__ == "__main__":
    create_positives_list()
