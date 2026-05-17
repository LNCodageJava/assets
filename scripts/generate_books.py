# python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from copy import deepcopy

INPUT = "pokopia_data.json"
TEMPLATE = "template.json"
OUT_DIR = "generated"

def fill_placeholders(components, prefix, items):
    """
    Remplace les composants dont le champ 'item' est 'prefixitemN' par items[N-1]
    ou par 'minecraft:birch_button' si la liste items est trop courte.
    """
    for comp in components:
        if comp.get("type") != "patchouli:item":
            continue
        item_name = comp.get("item", "")
        if item_name.startswith(prefix + "item"):
            try:
                idx = int(item_name[len(prefix + "item"):]) - 1
            except ValueError:
                continue
            comp["item"] = items[idx] if 0 <= idx < len(items) else "minecraft:birch_button"

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(TEMPLATE, "r", encoding="utf-8") as f:
        template = json.load(f)

    habitats = data.get("habitats", [])
    file_idx = 1
    for i in range(0, len(habitats) - 1, 2):
        h1 = habitats[i]
        h2 = habitats[i + 1]
        out = deepcopy(template)

        items1 = h1.get("hab", []) or []
        items2 = h2.get("hab", []) or []
        name1 = h1.get("name", f"hab_{i}")
        name2 = h2.get("name", f"hab_{i+1}")

        # Remplir les 9 emplacements pour chaque habitat (ou vide si manquant)
        fill_placeholders(out.get("components", []), "poke1", items1)
        fill_placeholders(out.get("components", []), "poke2", items2)

        # Remplacer les sprites
        for comp in out.get("components", []):
            if comp.get("type") == "patchouli:image":
                x = comp.get("x")
                y = comp.get("y")
                if x == 60 and y == 5:
                    comp["image"] = f"cobblemonfury:pokesprites/{name1}.png"
                elif x == 60 and y == 80:
                    comp["image"] = f"cobblemonfury:pokesprites/{name2}.png"

        # Nommer les fichiers de sortie séquentiellement 1-based : hab1.json, hab2.json, ...
        out_path = os.path.join(OUT_DIR, f"hab{file_idx}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        print(f"Généré: {out_path}")
        file_idx += 1

if __name__ == "__main__":
    main()
