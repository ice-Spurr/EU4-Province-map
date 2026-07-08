import re
import csv
from pathlib import Path

# 1. Chemins des fichiers
fichier_eu4 = r"save_default_1444-11-11.txt"
fichier_csv_entree = r"DEFAULT_values/provinces.csv"
fichier_csv_sortie = r"DEFAULT_values/provinces_review.csv"

# 2. Extraire les owners depuis le fichier .eu4
owners_dict = {}  # {ID_province: owner}

with open(fichier_eu4, "r", encoding="utf-8") as f:
    content = f.read()

# Regex pour capturer les blocs de province : -111={ ... owner="VEN" ... }
pattern_province = r'-(\d+)\s*=\s*\{[^}]*owner="([^"]+)"[^}]*\}'
for match in re.finditer(pattern_province, content):
    province_id, owner = match.groups()
    owners_dict[province_id] = owner

print(f"Extracted Owners : {len(owners_dict)} provinces")



# 3. Lire le CSV existant, mettre à jour la colonne owner, et trier par PROVID
with open(fichier_csv_entree, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    lignes = list(reader)

# Mettre à jour la colonne owner
for ligne in lignes:
    province_id = ligne["PROVID"]
    if province_id in owners_dict:
        ligne["owner"] = owners_dict[province_id]
        print(f"Updated : PROVID {province_id} -> owner = {owners_dict[province_id]}")

# Trier les lignes par PROVID (en numériques)
lignes_triees = sorted(lignes, key=lambda x: int(x["PROVID"]))



# 4. Écrire le CSV mis à jour
with open(fichier_csv_sortie, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, delimiter=";", fieldnames=lignes[0].keys())
    writer.writeheader()
    writer.writerows(lignes_triees)

print(f"CSV updated and sorted : {fichier_csv_sortie}")
