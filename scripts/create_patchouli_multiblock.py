import json
import string
import nbtlib

def convert_nbt_to_patchouli(nbt_path, output_path):
    # 1. Charger le fichier NBT du Structure Block
    nbt_file = nbtlib.load(nbt_path)
    root = nbt_file

    # Extraire les dimensions (X, Y, Z)
    size_x, size_y, size_z = [int(x) for x in root['size']]

    palette = root['palette']
    blocks = root['blocks']

    # Cartographier les coordonnées vers l'index de leur état de bloc
    block_grid = {}
    for b in blocks:
        pos = tuple(int(x) for x in b['pos'])
        block_grid[pos] = int(b['state'])

    # 2. Déterminer le bloc d'ancrage ('0')
    # Patchouli a besoin d'un point d'ancrage '0'. On cible le centre de la couche inférieure (y=0).
    anchor_x, anchor_y, anchor_z = size_x // 2, 0, size_z // 2
    anchor_state = block_grid.get((anchor_x, anchor_y, anchor_z), None)

    # Sécurité : Si le centre est vide, on prend le premier bloc non-air trouvé
    if anchor_state is None or str(palette[anchor_state]['Name']) in ["minecraft:air", "minecraft:structure_void"]:
        for b in blocks:
            s = int(b['state'])
            if str(palette[s]['Name']) not in ["minecraft:air", "minecraft:structure_void"]:
                anchor_state = s
                break

    # Pool de caractères pour le mapping (Lettres majuscules + chiffres sauf 0)
    char_pool = iter(string.ascii_uppercase + string.digits.replace('0', ''))

    state_to_char = {}
    mapping = {}

    # Assigner '0' à l'ancrage
    if anchor_state is not None:
        anchor_name = str(palette[anchor_state]['Name'])
        state_to_char[anchor_state] = "0"
        mapping["0"] = anchor_name

    # Assigner un caractère unique au reste de la palette
    for idx, tag in enumerate(palette):
        name = str(tag['Name'])
        if name in ["minecraft:air", "minecraft:structure_void"]:
            continue
        if idx in state_to_char:
            continue

        char = next(char_pool, None)
        if not char:
            raise ValueError("Trop de blocs uniques pour le format de Patchouli !")

        state_to_char[idx] = char
        mapping[char] = name

    # 3. Générer le pattern 3D (Couches Y, puis lignes Z, puis colonnes X)
    # Patchouli lit les couches du HAUT (Y max) vers le BAS (Y min)
    pattern = []
    for y in reversed(range(size_y)):
        layer = []
        for z in range(size_z):
            row_chars = []
            for x in range(size_x):
                state_idx = block_grid.get((x, y, z), None)

                if state_idx is None:
                    row_chars.append(" ") # Air par défaut
                else:
                    name = str(palette[state_idx]['Name'])
                    if name in ["minecraft:air", "minecraft:structure_void"]:
                        row_chars.append(" ")
                    else:
                        row_chars.append(state_to_char[state_idx])
            layer.append("".join(row_chars))
        pattern.append(layer)

    # 4. Injecter les données dans ton modèle JSON personnalisé
    patchouli_json = {
        "name": "充電器",
        "icon": mapping.get("0", "minecraft:stone"),
        "category": "cobblemonfury:capacity_category",
        "pages": [
            {
                "type": "multiblock",
                "name": "充電器的多方塊結構",
                "multiblock": {
                    "pattern": pattern,
                    "mapping": mapping
                }
            },
            {
                "type": "text",
                "text": "這是一些內部含有能源的物品:$(li)桶裝的液態靈魂$(li)神秘粉塵$(li)神秘樹葉$(li)神秘水晶棒$(li)水晶催化劑$(li)被囚禁的光$(li)螢石粉$(li)TNT$(li)煤炭$(li)經驗瓶$(br2)如果這些扔入的物品會產生副產品, 這些副產品將會從充電器頂部產出."
            },
            {
                "type": "crafting",
                "name": "充電器",
                "recipe": "minecraft:crafting_table"
            }
        ]
    }

    # Sauvegarder le résultat en conservant les caractères UTF-8 (chinois) intacts
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patchouli_json, f, ensure_ascii=False, indent=2)

    print(f" Converti avec succès ! Fichier sauvegardé dans : {output_path}")

    # 5. Mettre à jour pokopia_data.json
    update_pokopia_data(nbt_path, palette, blocks)

def update_pokopia_data(nbt_path, palette, blocks):
    import os

    # Extraire le nom du fichier NBT sans extension
    nbt_filename = os.path.basename(nbt_path).replace('.nbt', '')

    # Collecter tous les blocs présents dans la structure (avec duplicatas)
    biomes_list = []
    for b in blocks:
        state_idx = int(b['state'])
        block_name = str(palette[state_idx]['Name'])
        if block_name not in ["minecraft:air", "minecraft:structure_void"]:
            biomes_list.append(block_name)

    # Créer la nouvelle entrée mega_habitat
    new_entry = {
        "name": nbt_filename,
        "rotom": f"cobblemonfury:{nbt_filename}",
        "biomes": biomes_list
    }

    # Charger pokopia_data.json
    pokopia_path = "scripts/pokopia_data.json"
    with open(pokopia_path, 'r', encoding='utf-8') as f:
        pokopia_data = json.load(f)

    # Vérifier si une entrée avec ce nom existe déjà
    mega_habitats = pokopia_data.get("mega_habitats", [])
    existing_index = None
    for i, habitat in enumerate(mega_habitats):
        if habitat.get("name") == nbt_filename:
            existing_index = i
            break

    # Ajouter ou modifier l'entrée
    if existing_index is not None:
        mega_habitats[existing_index] = new_entry
        print(f" Entrée '{nbt_filename}' mise à jour dans pokopia_data.json")
    else:
        mega_habitats.append(new_entry)
        print(f" Nouvelle entrée '{nbt_filename}' ajoutée à pokopia_data.json")

    pokopia_data["mega_habitats"] = mega_habitats

    # Sauvegarder pokopia_data.json
    with open(pokopia_path, 'w', encoding='utf-8') as f:
        json.dump(pokopia_data, f, ensure_ascii=False, indent=2)

# --- Utilisation ---
# Remplace par les chemins de tes fichiers
convert_nbt_to_patchouli("scripts/rotom_farm.nbt", "rotom_farm.json")