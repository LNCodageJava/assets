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

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\blockstates\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Blockstate JSON generated at: {output_path}")


def copy_json(name: str):
    # Source file path (in same folder as this script)
    src_path = os.path.join(os.path.dirname(__file__), f"{name}.json")

    # Destination file path
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\models\block\{name}.json"
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
    dest_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\textures\block\{name}.png"

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

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\models\item\{name}.json"
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

    output_path = rf"C:\Users\garat\Documents\cobblemon_fury_neoforge\src\main\resources\assets\cobblemonfury\models\item\{folder}\{name}.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Item JSON generated at: {output_path}")

def generate_block(name:str):
    generate_blockstate(name)
    copy_json(name)
    copy_texture_png(name)
    generate_item_model(name)
    
generate_item("rune","dark1")
generate_item("rune","dark2")
generate_item("rune","dragon")
generate_item("rune","elec1")
generate_item("rune","elec2")
generate_item("rune","fight")
generate_item("rune","fire1")
generate_item("rune","fire2")
generate_item("rune","fire3")
generate_item("rune","ice")
generate_item("rune","plant1")
generate_item("rune","plant2")
generate_item("rune","poison1")
generate_item("rune","poison2")
generate_item("rune","psy")
generate_item("rune","rock1")
generate_item("rune","rock2")
generate_item("rune","water1")
generate_item("rune","water2")