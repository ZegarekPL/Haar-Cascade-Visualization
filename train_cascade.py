import os
import subprocess

base_dir = '/home/wiktor/Downloads/WIDER_train'
output_dir = os.path.join(base_dir, 'cascade')
positives_txt = os.path.join(base_dir, 'positives.txt')
negatives_txt = os.path.join(base_dir, 'bg.txt')
vec_file = os.path.join(base_dir, 'positives.vec')

sample_width = 24
sample_height = 24
num_samples = 1000
num_pos = 900
num_neg = 1000
num_stages = 10

os.makedirs(output_dir, exist_ok=True)

def create_vec_file():
    if not os.path.exists(vec_file):
        print("[*] Tworzę positives.vec...")
        command = [
            'opencv_createsamples',
            '-info', positives_txt,
            '-num', str(num_samples),
            '-w', str(sample_width),
            '-h', str(sample_height),
            '-vec', vec_file
        ]
        try:
            subprocess.run(command, check=True)
            print(f"[+] Stworzono positives.vec ({vec_file})")
        except subprocess.CalledProcessError as e:
            print(f"[!] Błąd podczas tworzenia positives.vec: {e}")
    else:
        print(f"[!] positives.vec już istnieje — pomijam tworzenie.")

def train_cascade():
    if os.listdir(output_dir):
        print(f"[!] Wygląda na to, że trening już był rozpoczęty.")
        decision = input("Czy chcesz wznowić trening? (y/n): ")
        if decision.lower() != 'y':
            print("[!] Przerywam.")
            return

    print("[*] Rozpoczynam trening Haar Cascade...")
    command = [
        'opencv_traincascade',
        '-data', output_dir,
        '-vec', vec_file,
        '-bg', negatives_txt,
        '-numPos', str(num_pos),
        '-numNeg', str(num_neg),
        '-numStages', str(num_stages),
        '-w', str(sample_width),
        '-h', str(sample_height),
        '-featureType', 'HAAR',
        '-mode', 'ALL'
    ]
    try:
        subprocess.run(command, check=True)
        print(f"[+] Trening zakończony! Plik XML zapisany w {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Błąd podczas treningu Haar Cascade: {e}")

if __name__ == "__main__":
    create_vec_file()
    train_cascade()
