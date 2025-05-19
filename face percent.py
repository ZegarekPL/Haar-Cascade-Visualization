import os
import xml.etree.ElementTree as ET

folder_z_xml = r'C:\Users\mazur\Downloads\baza_WK\fddb\pos'
minimalny_procent = 6
plik_wyjsciowy = "wynik.txt"

def oblicz_procent(xmin, ymin, xmax, ymax, szerokosc_img, wysokosc_img):
    pole_twarzy = (xmax - xmin) * (ymax - ymin)
    pole_obrazu = szerokosc_img * wysokosc_img
    return (pole_twarzy / pole_obrazu) * 100

# Zbierz wyniki
wyniki = []

for plik in os.listdir(folder_z_xml):
    if plik.endswith(".xml"):
        sciezka = os.path.join(folder_z_xml, plik)
        tree = ET.parse(sciezka)
        root = tree.getroot()

        szerokosc = int(root.find("size/width").text)
        wysokosc = int(root.find("size/height").text)

        nazwa_jpg = root.find("filename").text

        for obj in root.findall("object"):
            if obj.find("name").text == "face":
                bbox = obj.find("bndbox")
                xmin = int(bbox.find("xmin").text)
                ymin = int(bbox.find("ymin").text)
                xmax = int(bbox.find("xmax").text)
                ymax = int(bbox.find("ymax").text)

                procent = oblicz_procent(xmin, ymin, xmax, ymax, szerokosc, wysokosc)

                if procent >= minimalny_procent:
                    wyniki.append(nazwa_jpg)
                    break

with open(plik_wyjsciowy, "w") as f:
    for nazwa in wyniki:
        f.write(nazwa + "\n")

print(f"Zapisano {len(wyniki)} nazw plików do '{plik_wyjsciowy}'")
