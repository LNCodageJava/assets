#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from copy import deepcopy

INPUT = "pokopia_data.json"
TEMPLATE_HAB = "templates/template_spawn.json"     # Template pour les habitats (2 par page)
TEMPLATE_DESTROY = "templates/template_destroy.json" # Template pour les "destroy" (6 par page)
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

def process_pokemon_group(template, pokemon_list, file_prefix, file_idx):
    """
    Génère un fichier JSON pour un groupe contenant jusqu'à 6 Pokémon (utilisé pour destroy).
    """
    out = deepcopy(template)

    for slot_idx in range(1, 7):
        prefix = f"poke{slot_idx}"

        if slot_idx - 1 < len(pokemon_list):
            poke = pokemon_list[slot_idx - 1]
            name = poke.get("name", f"unknown_{slot_idx}")
            items = poke.get("items_to_display", [])

            fill_placeholders(out.get("components", []), prefix, items)

            for comp in out.get("components", []):
                if comp.get("type") == "patchouli:image":
                    if f"pokesprites/{prefix}.png" in comp.get("image", ""):
                        comp["image"] = f"cobblemonfury:pokesprites/{name}.png"
        else:
            fill_placeholders(out.get("components", []), prefix, [])
            for comp in out.get("components", []):
                if comp.get("type") == "patchouli:image" and f"pokesprites/{prefix}.png" in comp.get("image", ""):
                    comp["image"] = "cobblemonfury:pokesprites/0_break.png"

    out_path = os.path.join(OUT_DIR, f"{file_prefix}{file_idx}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Généré: {out_path}")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    # On charge les deux fichiers de template séparément
    with open(TEMPLATE_HAB, "r", encoding="utf-8") as f:
        template_hab = json.load(f)

    with open(TEMPLATE_DESTROY, "r", encoding="utf-8") as f:
        template_destroy = json.load(f)

    # ---------------------------------------------------------
    # PARTIE 1 : Génération des Habitats (Template Habitat)
    # ---------------------------------------------------------
    habitats = data.get("habitats", [])
    hab_idx = 1
    for i in range(0, len(habitats) - 1, 2):
        h1 = habitats[i]
        h2 = habitats[i + 1]

        # On utilise spécifiquement le template des habitats ici
        out = deepcopy(template_hab)

        items1 = h1.get("hab", []) or []
        items2 = h2.get("hab", []) or []
        name1 = h1.get("name", f"hab_{i}")
        name2 = h2.get("name", f"hab_{i+1}")

        fill_placeholders(out.get("components", []), "poke1", items1)
        fill_placeholders(out.get("components", []), "poke2", items2)

        for comp in out.get("components", []):
            if comp.get("type") == "patchouli:image":
                x = comp.get("x")
                y = comp.get("y")
                if x == 60 and y == 5:
                    comp["image"] = f"cobblemonfury:pokesprites/{name1}.png"
                elif x == 60 and y == 80:
                    comp["image"] = f"cobblemonfury:pokesprites/{name2}.png"

        out_path = os.path.join(OUT_DIR, f"hab{hab_idx}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Généré: {out_path}")
        hab_idx += 1

    # ---------------------------------------------------------
    # PARTIE 2 : Génération des Capacités "Destroy" (Template Destroy)
    # ---------------------------------------------------------
    capacities = data.get("capacities", [])

    destroy_pokemon = []
    for cap in capacities:
        if cap.get("ability") == "destroy":
            destroy_pokemon.append({
                "name": cap.get("name"),
                "items_to_display": cap.get("blocks", [])
            })

    destroy_idx = 1
    for i in range(0, len(destroy_pokemon), 6):
        chunk = destroy_pokemon[i:i+6]
        # On passe template_destroy en argument à la fonction
        process_pokemon_group(template_destroy, chunk, "destroy", destroy_idx)
        destroy_idx += 1

if __name__ == "__main__":
    main()