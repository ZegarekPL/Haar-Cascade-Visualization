import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from utils import resize_image, draw_boundary

# === Przygotowanie detekcji ===
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def add_gaussian_blur(img):
    return cv2.GaussianBlur(img, (11, 11), 0)

def add_salt_pepper_noise(img, amount=0.02):
    noisy = img.copy()
    num_salt = np.ceil(amount * img.size * 0.5).astype(int)
    coords = [np.random.randint(0, i - 1, num_salt) for i in img.shape[:2]]
    noisy[coords[0], coords[1]] = 255
    num_pepper = np.ceil(amount * img.size * 0.5).astype(int)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in img.shape[:2]]
    noisy[coords[0], coords[1]] = 0
    return noisy

def add_stripes(img):
    striped = img.copy()
    alpha = 0.3  # przezroczystość (0 - całkowicie przezroczysty, 1 - całkowicie widoczny)
    stripe_width = 10

    for i in range(0, img.shape[1], 30):  # co 30 pikseli rysujemy pasek
        overlay = striped.copy()
        cv2.rectangle(overlay, (i, 0), (i + stripe_width, img.shape[0]), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, striped, 1 - alpha, 0, striped)

    return striped


def add_random_noise(img):
    noise = np.random.normal(0, 25, img.shape).astype(np.uint8)
    return cv2.add(img, noise)

# === GUI z Tkinter ===
class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detekcja twarzy z zakłóceniami")
        self.index = 0
        self.results = []

        # Obraz
        self.image_label = tk.Label(root)
        self.image_label.pack()

        # Opis
        self.info_label = tk.Label(root, text="", font=("Arial", 14))
        self.info_label.pack(pady=10)

        # Przyciski sterujące
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.prev_btn = tk.Button(btn_frame, text="<< Poprzedni", command=self.prev_image)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(btn_frame, text="Następny >>", command=self.next_image)
        self.next_btn.grid(row=0, column=1, padx=10)

        self.load_btn = tk.Button(root, text="Wczytaj zdjęcie", command=self.load_image)
        self.load_btn.pack(pady=10)

        self.quit_btn = tk.Button(root, text="Zamknij", command=root.quit)
        self.quit_btn.pack(pady=10)

    def cv_to_tk(self, cv_img):
        bgr_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(bgr_img)
        tk_img = ImageTk.PhotoImage(pil_img)
        return tk_img

    def show_image(self):
        if self.results:
            label, img, count = self.results[self.index]
            img_tk = self.cv_to_tk(img)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk  # zapobiega usunięciu przez GC

            self.info_label.config(text=f"[{self.index+1}/{len(self.results)}] {label} — Wykryto twarzy: {count}")

    def next_image(self):
        if self.results:
            self.index = (self.index + 1) % len(self.results)
            self.show_image()

    def prev_image(self):
        if self.results:
            self.index = (self.index - 1) % len(self.results)
            self.show_image()

    def load_image(self):
        # Wybór pliku
        file_path = filedialog.askopenfilename(title="Wybierz zdjęcie", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])

        if file_path:
            # Wczytanie obrazu
            original = cv2.imread(file_path)

            if original is None:
                print(f"Błąd: Nie można załadować obrazu z ścieżki: {file_path}")
                return

            # Przetwarzanie zdjęć
            original_resized = resize_image(original)

            tests = {
                "Oryginał": original_resized,
                "Rozmycie Gaussa": add_gaussian_blur(original_resized),
                "Szum sol-pieprz": add_salt_pepper_noise(original_resized),
                "Paski": add_stripes(original_resized),
                "Ziarno": add_random_noise(original_resized),
            }

            self.results = []
            for label, img in tests.items():
                img_copy = img.copy()
                coords, img_with_box = draw_boundary(img_copy, faceCascade, 1.1, 10, (255, 0, 0), "Face")
                count = len(coords)
                self.results.append((label, img_with_box, count))

            # Pokaż pierwsze zdjęcie
            self.index = 0
            self.show_image()

# Uruchomienie GUI
root = tk.Tk()
app = FaceApp(root)
root.mainloop()
