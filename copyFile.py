import os
import shutil
import random

folderA = r'C:\Users\mazur\Downloads\baza_WK\fddb\neg'
folderB = r'C:\Users\mazur\Downloads\baza_WK\fddb\n'
liczba_plikow = 251

os.makedirs(folderB, exist_ok=True)

wszystkie_pliki = [f for f in os.listdir(folderA) if f.lower().endswith('.jpg')]

liczba_do_pobr = min(liczba_plikow, len(wszystkie_pliki))

wylosowane = random.sample(wszystkie_pliki, liczba_do_pobr)

for plik in wylosowane:
    src = os.path.join(folderA, plik)
    dst = os.path.join(folderB, plik)
    shutil.copy2(src, dst)

print(f'✅ Skopiowano {liczba_do_pobr} plików z {folderA} do {folderB}')
