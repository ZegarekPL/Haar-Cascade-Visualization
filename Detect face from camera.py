import cv2

from utils import detect_face

#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier('cascade50.xml')           # błąd
#faceCascade = cv2.CascadeClassifier('cascade50_10stage.xml')   #
#faceCascade = cv2.CascadeClassifier('cascade100.xml')          #
#faceCascade = cv2.CascadeClassifier('cascade200.xml')          #
faceCascade = cv2.CascadeClassifier('cascade200_inne.xml')      # inne zdjęcia

video_capture = cv2.VideoCapture(0)

while True:
    _, image = video_capture.read()
    image = detect_face(image, faceCascade)
    cv2.imshow('Face detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()