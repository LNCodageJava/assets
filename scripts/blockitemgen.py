import os


import os
import json
import shutil



# STARDUST
# {"type": "patchouli:item", "item": "poke1item1", "framed": false, "x": 40, "y": Y},
# {"type": "patchouli:item", "item": "poke1item2", "framed": false, "x": 60, "y": Y},
# {"type": "patchouli:text", "text": "poke1price", "x": 80, "y": Y},
# {"type": "patchouli:text", "text": "poke1maxValue", "x": 100, "y": Y}

# DESTROY
# {"type": "patchouli:item", "item": "poke1item1", "framed": false, "x": 60, "y": Y+20},
# {"type": "patchouli:item", "item": "poke1item2", "framed": false, "x": 80, "y": Y+20},
# {"type": "patchouli:item", "item": "poke1item3", "framed": false, "x": 100, "y": Y+20},
# {"type": "patchouli:image", "image": "cobblemonfury:pokesprites/0_break.png", "width": 48, "height": 48, "texture_width": 48, "texture_height": 48, "x": 22, "y": Y},
#
# PLACE
# {"type": "patchouli:item", "item": "poke1item1", "framed": false, "x": 60, "y": Y+20},
# {"type": "patchouli:item", "item": "poke1item2", "framed": false, "x": 80, "y": Y+20},
# {"type": "patchouli:item", "item": "poke1item3", "framed": false, "x": 100, "y": Y+20},
# {"type": "patchouli:image", "image": "cobblemonfury:pokesprites/0_transform.png", "width": 48, "height": 48, "texture_width": 48, "texture_height": 48, "x": 22, "y": Y},


cobblemonfury:pokesprites/0_transform.png
def generate_blockstate(name: str):
    data = {
        "variants": {
            "": {
                "model": f"cobblemonfury:block/{name}"
            }
        }
    }

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\blockstates\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Blockstate JSON generated at: {output_path}")


def copy_json(name: str):
    # Source file path (in same folder as this script)
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.json")

    # Destination file path
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\models\block\{name}.json"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Charger et modifier le JSON
    with open(src_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "textures" in data:
        data["textures"] = {
            "0": f"cobblemonfury:block/{name}",
            "particle": f"cobblemonfury:block/{name}"
        }

    # Sauvegarder le fichier modifié
    with open(dest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Block model JSON copied & updated at: {dest_path}")

def copy_texture_png(name: str):
    # Chercher d'abord dans bbmodels/justTextures
    script_dir = os.path.dirname(__file__)
    src_path_bbmodels = os.path.join(os.path.dirname(script_dir), "bbmodels", "justTextures", f"{name}.png")

    # Si non trouvé, chercher dans le dossier du script
    if os.path.exists(src_path_bbmodels):
        src_path = src_path_bbmodels
    else:
        src_path = os.path.join(script_dir, f"{name}.png")

    # Destination path
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\textures\block\{name}.png"

    # Ensure destination folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Copy the PNG file
    shutil.copyfile(src_path, dest_path)

    print(f"✅ Texture PNG copied to: {dest_path}")


import os
import json

def generate_item_model(name: str):
    data = {
        "parent": f"cobblemonfury:block/{name}",
        "display": {
            "thirdperson": {
                "rotation": [10, -45, 170],
                "translation": [0, 1.5, -2.75],
                "scale": [0.375, 0.375, 0.375]
            }
        }
    }

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\models\item\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Item model JSON generated at: {output_path}")


def generate_item(folder:str,name: str):
    data = {
  "parent": "item/generated",
  "textures": {
    "layer0": f"cobblemonfury:item/{folder}/{name}"
        }
    }

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\models\item\{folder}\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Item JSON generated at: {output_path}")

    # Copy texture PNG
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.png")
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\textures\item\{folder}\{name}.png"
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copyfile(src_path, dest_path)
    print(f"✅ Item texture PNG copied to: {dest_path}")

def generate_block(name:str):
    generate_blockstate(name)
    copy_json(name)
    copy_texture_png(name)
    generate_item_model(name)
    generate_block_loot_table(name)


def generate_block_model_from_template(name: str):
    # Le template basé sur ton JSON, avec le nom de texture dynamique
    data = {
        "parent": "block/block",
        "textures": {
            "particle": f"cobblemonfury:block/{name}",
            "texture": f"cobblemonfury:block/{name}"
        },
        "elements": [
            {
                "from": [0, 0, 0],
                "to": [16, 16, 16],
                "faces": {
                    "down":  {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "down"},
                    "up":    {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "up"},
                    "north": {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "north"},
                    "south": {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "south"},
                    "west":  {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "west"},
                    "east":  {"uv": [0, 0, 16, 16], "texture": "#texture", "cullface": "east"}
                }
            }
        ]
    }

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\assets\cobblemonfury\models\block\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Block model JSON generated from template at: {output_path}")


def generate_block_loot_table(name: str):
    """Génère la loot table permettant au bloc de se drop lui-même."""
    data = {
        "type": "minecraft:block",
        "random_sequence": f"cobblemonfury:blocks/{name}",
        "pools": [
            {
                "rolls": 1.0,
                "conditions": [
                    {
                        "condition": "minecraft:survives_explosion"
                    }
                ],
                "entries": [
                    {
                        "type": "minecraft:item",
                        "name": f"cobblemonfury:{name}"
                    }
                ]
            }
        ]
    }

    # Chemin pour les tables de butin en 1.21.1 (le dossier s'appelle généralement 'blocks' au pluriel)
    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_2_fabric\src\main\resources\data\cobblemonfury\loot_table\blocks\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Loot table JSON generated at: {output_path}")

def generate_block_without_model(name: str):
    """Génère blockstate, modèle de bloc (via template), copie la texture et modèle d'item"""
    generate_blockstate(name)
    generate_block_model_from_template(name) # Utilise le template au lieu de copier un fichier
    copy_texture_png(name)
    generate_item_model(name)
    generate_block_loot_table(name)


generate_block_without_model("island_generator_base")
# generate_item("produced","smoothie_green")
# generate_item("produced","smoothie_yellow")
# generate_item("produced","smoothie_red")
# generate_item("produced","smoothie_blue")
# generate_item("produced","smoothie_white")
# generate_item("produced","soup_carrot")
# generate_item("produced","soup_potato")
# generate_item("produced","soup_wheat")
# generate_item("produced","wood_birch")
# generate_item("produced","wood_jungle")
# generate_item("produced","wood_oak")
# generate_item("produced","wood_spruce")
# generate_item("produced","wood_cherry")