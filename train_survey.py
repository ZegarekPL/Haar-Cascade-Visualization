import cv2
import os
import time
import numpy as np

image_dir = "train_positive/filtered_images"
cascade_path = "classifier_output1/cascade.xml"
num_images = 12
grid_cols = 4  # np. 4 kolumny, 3 wiersze = 12 zdjęć

face_cascade = cv2.CascadeClassifier(cascade_path)
if face_cascade.empty():
    print("Nie udało się załadować klasyfikatora.")
    exit()

images = sorted([
    f for f in os.listdir(image_dir)
    if f.lower().endswith(('.jpg', '.png'))
])[:num_images]

processed_images = []
total_start_time = time.time()

for idx, img_name in enumerate(images):
    img_path = os.path.join(image_dir, img_name)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Nie można wczytać: {img_path}")
        continue

    img = cv2.resize(img, (300, 300))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    start_time = time.time()
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    elapsed = time.time() - start_time
    print(f"[{idx+1}/{num_images}] {img_name}: {elapsed:.3f} sekundy")

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    img_resized = cv2.resize(img, (300, 300))
    processed_images.append(img_resized)

total_time = time.time() - total_start_time
print(f"\n✅ Całkowity czas dla 12 obrazów: {total_time:.2f} sekundy")

grid_rows = int(np.ceil(len(processed_images) / grid_cols))
blank = np.zeros_like(processed_images[0])

while len(processed_images) < grid_rows * grid_cols:
    processed_images.append(blank)

rows = []
for i in range(grid_rows):
    row = np.hstack(processed_images[i*grid_cols:(i+1)*grid_cols])
    rows.append(row)

grid_image = np.vstack(rows)

cv2.imshow("Wszystkie 12 zdjęć z rozpoznaniem twarzy", grid_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
