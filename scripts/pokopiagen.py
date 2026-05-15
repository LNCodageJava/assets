import pandas as pd
import json
from pathlib import Path

def clean_namespace(val):
    """Applique les règles de namespace sur les identifiants de blocs."""
    val = str(val).strip()

    if val.startswith("cby:"):
        return val.replace("cby:", "cobblemonfury:", 1)
    elif val.startswith("cb:"):
        return val.replace("cb:", "cobblemon:", 1)
    elif ":" not in val:
        return f"minecraft:{val}"

    return val

def generate_habitat_json(excel_file_name, output_json_name):
    base_dir = Path(__file__).resolve().parent
    excel_path = base_dir / excel_file_name
    output_path = base_dir / output_json_name

    try:
        # On lit le fichier (Assure-toi que le nom de la feuille est correct)
        df = pd.read_excel(excel_path, sheet_name='Feuille 1')
    except Exception as e:
        print(f"Erreur : {e}")
        return

    habitats_list = []
    hab_columns = [col for col in df.columns if str(col).startswith('HAB')]

    for _, row in df.iterrows():
        name = row['NAME']
        if pd.isna(name) or str(name).strip().upper() == 'TODO':
            continue

        habs = []
        for col in hab_columns:
            val = row[col]
            if pd.notna(val) and str(val).strip().upper() != 'TODO':
                # On applique la transformation du namespace ici
                habs.append(clean_namespace(val))

        if habs:
            habitats_list.append({
                "name": str(name).lower().strip(),
                "hab": habs
            })

    result = {"habitats": habitats_list}

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Fichier généré avec namespaces corrigés : {output_path}")

# Lancement
generate_habitat_json("pokomons.xlsx", "habitats.json")