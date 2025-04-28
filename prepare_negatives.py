import os
from tqdm import tqdm

base_dir = '/home/wiktor/Downloads/WIDER_train'
negative_dir = os.path.join(base_dir, 'negative')
negatives_txt = os.path.join(base_dir, 'bg.txt')


def create_negatives_list():
    with open(negatives_txt, 'w') as f:
        neg_files = []
        for root, dirs, files in os.walk(negative_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    neg_files.append(os.path.join(root, file))

        for file_path in tqdm(neg_files, desc="Tworzenie bg.txt"):
            f.write(file_path + '\n')
    print(f"[+] Stworzono negatives.txt ({negatives_txt})")


if __name__ == "__main__":
    create_negatives_list()
