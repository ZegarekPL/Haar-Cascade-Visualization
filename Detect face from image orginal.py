import cv2
from utils import resize_image, detect_face

#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('cascade50.xml')           # błąd
#faceCascade = cv2.CascadeClassifier('cascade50_10stage.xml')   #
#faceCascade = cv2.CascadeClassifier('cascade100.xml')          #
#faceCascade = cv2.CascadeClassifier('cascade200.xml')          #
faceCascade = cv2.CascadeClassifier('cascade200_inne.xml')      # inne zdjęcia

image_path = 'test4.jpeg'

image = cv2.imread(image_path)

if image is None:
    print(f"Błąd: Nie można załadować obrazu z ścieżki: {image_path}")
else:
    image = resize_image(image)
    image = detect_face(image, faceCascade)

    cv2.imshow('Face detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()