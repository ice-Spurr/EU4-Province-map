import re
import csv
from pathlib import Path

# 1. Dossiers
dossier_tags = "Europa Universalis 4/history/countries"  # Contient "ADA - Adal.txt", etc.
dossier_couleurs = "Europa Universalis 4/common/countries"  # Contient "Adal.txt", etc.
fichier_sortie = "extracted_colors.csv"

# 2. Extraire les tags depuis les fichiers "TAG - Nom.txt"
tags_dict = {}
for fichier in Path(dossier_tags).glob("*.txt"):
    nom_fichier = fichier.name.replace(".txt", "")
    if " - " in nom_fichier:
        tag, nom_province = nom_fichier.split(" - ", 1)
        tags_dict[nom_province] = tag
    else:
        print(f"File ignored (invalid format) : {fichier.name}")

# 3. Extraire les couleurs depuis les fichiers "Nom.txt"
def extraire_couleurs(content):
    match = re.search(r'color\s*=\s*\{\s*(\d{1,3})\s*(\d{1,3})\s*(\d{1,3})\s*\}', content)
    return match.groups() if match else (None, None, None)

# 4. Créer le CSV final
champs_csv = ["nom_province", "tag", "R", "G", "B"]

with open(fichier_sortie, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(champs_csv)

    for fichier in Path(dossier_couleurs).glob("*.txt"):
        nom_province = fichier.name.replace(".txt", "")
        with open(fichier, "r", encoding="Windows-1252") as f:
            content = f.read()

        r, g, b = extraire_couleurs(content)
        tag = tags_dict.get(nom_province, "")  # Tag vide si non trouvé

        if r is not None:  # On écrit seulement si on a trouvé des couleurs
            writer.writerow([nom_province, tag, r, g, b])
            print(f"OK {nom_province} -> Tag: {tag}, RGB: ({r}, {g}, {b})")
        else:
            print(f"⚠NO color found in {fichier.name}")

print(f"Extraction successful ! Result in {fichier_sortie}")