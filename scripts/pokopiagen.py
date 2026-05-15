import pandas as pd
import json
from pathlib import Path

def generate_habitat_json(excel_file_name, output_json_name):
    # Gestion du chemin relatif : on cible le dossier où se trouve ce script
    base_dir = Path(__file__).resolve().parent
    excel_path = base_dir / excel_file_name
    output_path = base_dir / output_json_name

    # Lecture du fichier Excel
    try:
        df = pd.read_excel(excel_path, sheet_name='Feuille 1')
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    habitats_list = []

    # Identification automatique des colonnes HAB1, HAB2...
    hab_columns = [col for col in df.columns if str(col).startswith('HAB')]

    for _, row in df.iterrows():
        name = row['NAME']

        # Skip si le nom est vide ou est un TODO
        if pd.isna(name) or str(name).strip().upper() == 'TODO':
            continue

        # Extraction des habitats valides
        habs = []
        for col in hab_columns:
            val = row[col]
            if pd.notna(val) and str(val).strip().upper() != 'TODO':
                habs.append(str(val).strip())

        # Ajout au dictionnaire si au moins un habitat est trouvé
        if habs:
            habitats_list.append({
                "name": str(name).lower().strip(),
                "hab": habs
            })

    # Construction du résultat final
    result = {"habitats": habitats_list}

    # Écriture physique du fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Succès ! Fichier généré ici : {output_path}")

# Utilisation avec les noms de fichiers (assurez-vous qu'ils sont dans le même dossier)
generate_habitat_json("pokomons.xlsx", "habitats.json")