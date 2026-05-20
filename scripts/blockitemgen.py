import os


import os
import json
import shutil

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
    # Source file path in same folder as script
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.png")

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

def generate_block(name:str):
    generate_blockstate(name)
    copy_json(name)
    copy_texture_png(name)
    generate_item_model(name)


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

def generate_block_without_model(name: str):
    """Génère blockstate, modèle de bloc (via template), copie la texture et modèle d'item"""
    generate_blockstate(name)
    generate_block_model_from_template(name) # Utilise le template au lieu de copier un fichier
    copy_texture_png(name)
    generate_item_model(name)

# Utilisation
generate_block_without_model("labo_2")