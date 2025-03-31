import cv2

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords, img

def detect_face(img, faceCascade):
    color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
    coords, img = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    return img

def resize_image(img, max_height=800):
    height, width = img.shape[:2]
    if height <= max_height:
        return img
    new_width = int(width * (max_height / height))
    resized_img = cv2.resize(img, (new_width, max_height))
    return resized_img
