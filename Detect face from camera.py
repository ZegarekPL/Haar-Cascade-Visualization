import cv2

from utils import detect_face

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(-1)

while True:
    _, image = video_capture.read()
    image = detect_face(image, faceCascade)
    cv2.imshow('Face detection', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()