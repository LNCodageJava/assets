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
    anchor_pos = (anchor_x, anchor_y, anchor_z)
    anchor_state = block_grid.get(anchor_pos, None)

    # Sécurité : Si le centre est vide, on prend le premier bloc non-air trouvé
    if anchor_state is None or str(palette[anchor_state]['Name']) in ["minecraft:air", "minecraft:structure_void"]:
        for b in blocks:
            s = int(b['state'])
            if str(palette[s]['Name']) not in ["minecraft:air", "minecraft:structure_void"]:
                anchor_pos = tuple(int(x) for x in b['pos'])
                anchor_state = s
                break

    # Pool de caractères pour le mapping (Lettres majuscules + chiffres sauf 0)
    char_pool = iter(string.ascii_uppercase + string.digits.replace('0', ''))

    state_to_char = {}
    mapping = {}

    # Fonction pour construire le nom complet du bloc avec ses propriétés
    def get_block_name_with_properties(tag):
        name = str(tag['Name'])
        if 'Properties' in tag and tag['Properties']:
            props = tag['Properties']
            prop_list = [f"{k}={v}" for k, v in props.items()]
            return f"{name}[{','.join(prop_list)}]"
        return name

    # Assigner '0' à l'ancrage dans le mapping
    if anchor_state is not None:
        anchor_name = get_block_name_with_properties(palette[anchor_state])
        mapping["0"] = anchor_name

    # Assigner un caractère unique à TOUTE la palette (y compris le type d'ancrage)
    for idx, tag in enumerate(palette):
        name = str(tag['Name'])
        if name in ["minecraft:air", "minecraft:structure_void"]:
            continue

        char = next(char_pool, None)
        if not char:
            raise ValueError("Trop de blocs uniques pour le format de Patchouli !")

        state_to_char[idx] = char
        mapping[char] = get_block_name_with_properties(tag)

    # 3. Générer le pattern 3D (Couches Y, puis lignes Z, puis colonnes X)
    # Patchouli lit les couches du HAUT (Y max) vers le BAS (Y min)
    pattern = []
    for y in reversed(range(size_y)):
        layer = []
        for z in range(size_z):
            row_chars = []
            for x in range(size_x):
                pos = (x, y, z)
                state_idx = block_grid.get(pos, None)

                # Si c'est la position d'ancrage, utiliser '0'
                if pos == anchor_pos:
                    row_chars.append("0")
                elif state_idx is None:
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
            "Topaste":{
                "type": "multiblock",
                "name": "充電器的多方塊結構",
                "multiblock": {
                    "pattern": pattern,
                    "mapping": mapping
                },
                "text": "器的多",
            }
    }

    # Sauvegarder le résultat en conservant les caractères UTF-8 (chinois) intacts
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(patchouli_json, f, ensure_ascii=False, indent=2)

    print(f" Converti avec succès ! Fichier sauvegardé dans : {output_path}")

    # 5. Mettre à jour pokopia_data.json

# --- Utilisation ---
# Remplace par les chemins de tes fichiers
convert_nbt_to_patchouli("patchouli/multiblocks/w_agriculture.nbt", "patchouli/generated/w_agriculture.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_badlands.nbt", "patchouli/generated/w_badlands.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_desert.nbt", "patchouli/generated/w_desert.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_fire.nbt", "patchouli/generated/w_fire.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_fossils.nbt", "patchouli/generated/w_fossils.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_gem.nbt", "patchouli/generated/w_gem.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_jungle.nbt", "patchouli/generated/w_jungle.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_marais.nbt", "patchouli/generated/w_marais.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_mossy.nbt", "patchouli/generated/w_mossy.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_nether_cave.nbt", "patchouli/generated/w_nether_cave.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_plains.nbt", "patchouli/generated/w_plains.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_rocky.nbt", "patchouli/generated/w_rocky.json")
convert_nbt_to_patchouli("patchouli/multiblocks/w_underwater.nbt", "patchouli/generated/w_underwater.json")