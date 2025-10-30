import os
import shutil

folder_z_jpg = r'C:\Users\mazur\Downloads\baza_WK\fddb\pos'
plik_z_listą = 'wynik.txt'
folder_docelowy = r'C:\Users\mazur\Downloads\baza_WK\fddb\p'

os.makedirs(folder_docelowy, exist_ok=True)

with open(plik_z_listą, 'r') as f:
    pliki = [linia.strip() for linia in f if linia.strip()]

ile_znalezionych = 0
for nazwa in pliki:
    sciezka_zrodlo = os.path.join(folder_z_jpg, nazwa)
    sciezka_docelowa = os.path.join(folder_docelowy, nazwa)

    if os.path.isfile(sciezka_zrodlo):
        shutil.copy2(sciezka_zrodlo, sciezka_docelowa)
        ile_znalezionych += 1
    else:
        print(f'❌ Nie znaleziono: {nazwa}')

print(f'✅ Skopiowano {ile_znalezionych} plików do: {folder_docelowy}')
