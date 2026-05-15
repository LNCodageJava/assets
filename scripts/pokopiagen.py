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

def generate_mod_data_json(excel_file_name, output_json_name):
    base_dir = Path(__file__).resolve().parent
    excel_path = base_dir / excel_file_name
    output_path = base_dir / output_json_name

    try:
        df = pd.read_excel(excel_path, sheet_name='Feuille 1')
    except Exception as e:
        print(f"Erreur : {e}")
        return

    habitats_list = []
    capacities_list = []

    # Identification des colonnes
    hab_columns = [col for col in df.columns if str(col).startswith('HAB')]
    block_columns = [col for col in df.columns if str(col).startswith('BLOCK')]

    for _, row in df.iterrows():
        # --- CONDITION BIO ---
        # Si la colonne BIO est vide, on passe directement à la ligne suivante
        if pd.isna(row.get('BIO')) or str(row.get('BIO')).strip() == "":
            continue

        name = str(row['NAME']).lower().strip() if pd.notna(row['NAME']) else None
        ability = str(row['ABILITY']).strip() if pd.notna(row['ABILITY']) else None

        if not name or name.upper() == 'TODO':
            continue

        # --- Section HABITATS ---
        habs = []
        for col in hab_columns:
            val = row[col]
            if pd.notna(val) and str(val).strip().upper() != 'TODO':
                habs.append(clean_namespace(val))

        if habs:
            habitats_list.append({
                "name": name,
                "hab": habs
            })

        # --- Section CAPACITIES ---
        blocks = []
        for col in block_columns:
            val = row[col]
            if pd.notna(val) and str(val).strip().upper() != 'TODO':
                blocks.append(clean_namespace(val))

        if ability or blocks:
            capacities_list.append({
                "name": name,
                "ability": ability if ability and ability.upper() != 'TODO' else "",
                "blocks": blocks
            })

    # Construction du dictionnaire final
    result = {
        "habitats": habitats_list,
        "capacities": capacities_list
    }

    # Écriture du fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Fichier généré (Filtrage BIO actif) : {output_path}")

# Lancement
generate_mod_data_json("pokomons.xlsx", "pokopia_data.json")