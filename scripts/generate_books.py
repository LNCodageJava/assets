#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from copy import deepcopy

INPUT = "pokopia_data.json"
TEMPLATE_HAB = "templates/template_spawn.json"
TEMPLATE_DESTROY = "templates/template_destroy.json"
TEMPLATE_TRANSFORM = "templates/template_transform.json"
TEMPLATE_MEGA_HABITAT = "templates/template_mega_habitat.json"
OUT_DIR = "generated"

def fill_placeholders(components, prefix, items, fallback="minecraft:birch_button"):
    """
    Remplace les composants dont le champ 'item' est 'prefixitemN' par items[N-1].
    Si fallback est None et que la liste est trop courte, on retire ou on vide le composant.
    """
    kept_components = []
    for comp in components:
        if comp.get("type") != "patchouli:item":
            kept_components.append(comp)
            continue

        item_name = comp.get("item", "")
        if item_name.startswith(prefix + "item"):
            try:
                idx = int(item_name[len(prefix + "item"):]) - 1
            except ValueError:
                kept_components.append(comp)
                continue

            if 0 <= idx < len(items):
                comp["item"] = items[idx]
                kept_components.append(comp)
            elif fallback is not None:
                comp["item"] = fallback
                kept_components.append(comp)
            else:
                # Si fallback est None, on ne garde pas le composant d'item (laisse vide)
                continue
        else:
            kept_components.append(comp)

    # On met à jour la liste des composants directement si nécessaire
    components[:] = kept_components

def process_pokemon_group(template, pokemon_list, file_prefix, file_idx):
    """
    Génère un fichier JSON pour un groupe contenant jusqu'à 6 Pokémon (utilisé pour destroy).
    """
    out = deepcopy(template)
    components = out.get("components", [])

    for slot_idx in range(1, 7):
        prefix = f"poke{slot_idx}"

        if slot_idx - 1 < len(pokemon_list):
            # Le Pokémon existe pour ce slot
            poke = pokemon_list[slot_idx - 1]
            name = poke.get("name", f"unknown_{slot_idx}")
            items = poke.get("items_to_display", [])

            # Pas de birch_button pour le destroy -> fallback=None
            fill_placeholders(components, prefix, items, fallback=None)

            for comp in components:
                if comp.get("type") == "patchouli:image":
                    if f"pokesprites/{prefix}.png" in comp.get("image", ""):
                        comp["image"] = f"cobblemonfury:pokesprites/{name}.png"
        else:
            # Aucun Pokémon pour ce slot : on n'affiche ni items, ni image de bris de bloc (0_break)
            fill_placeholders(components, prefix, [], fallback=None)

            # On supprime purement et simplement le composant image de ce slot pour qu'il soit invisible
            components = [
                comp for comp in components
                if not (comp.get("type") == "patchouli:image" and f"pokesprites/{prefix}.png" in comp.get("image", ""))
            ]

    out["components"] = components
    out_path = os.path.join(OUT_DIR, f"{file_prefix}{file_idx}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Généré: {out_path}")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(TEMPLATE_HAB, "r", encoding="utf-8") as f:
        template_hab = json.load(f)

    with open(TEMPLATE_DESTROY, "r", encoding="utf-8") as f:
        template_destroy = json.load(f)

    with open(TEMPLATE_TRANSFORM, "r", encoding="utf-8") as f:
        template_transform = json.load(f)

    with open(TEMPLATE_MEGA_HABITAT, "r", encoding="utf-8") as f:
        template_mega_habitat = json.load(f)

    # ---------------------------------------------------------
    # PARTIE 1 : Génération des Habitats (Template Habitat)
    # ---------------------------------------------------------
    habitats = data.get("habitats", [])
    hab_idx = 1
    for i in range(0, len(habitats) - 1, 2):
        h1 = habitats[i]
        h2 = habitats[i + 1]

        out = deepcopy(template_hab)

        items1 = h1.get("hab", []) or []
        items2 = h2.get("hab", []) or []
        name1 = h1.get("name", f"hab_{i}")
        name2 = h2.get("name", f"hab_{i+1}")

        # On garde le comportement par défaut (birch_button) pour les habitats
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
        process_pokemon_group(template_destroy, chunk, "destroy", destroy_idx)
        destroy_idx += 1

    transform_pokemon = []
    for cap in capacities:
        if cap.get("ability") == "transform":
            transform_pokemon.append({
                "name": cap.get("name"),
                "items_to_display": cap.get("blocks", [])
            })

    transform_idx = 1
    for i in range(0, len(transform_pokemon), 6):
        chunk = transform_pokemon[i:i+6]
        process_pokemon_group(template_transform, chunk, "transform", transform_idx)
        transform_idx += 1

    # ---------------------------------------------------------
    # PARTIE 3 : Génération des Mega Habitats
    # ---------------------------------------------------------
    mega_habitats = data.get("mega_habitats", [])
    mega_idx = 1
    for mega in mega_habitats:
        out = deepcopy(template_mega_habitat)
        components = out.get("components", [])

        block_list = mega.get("blockList", [])
        recipes = mega.get("recipe", [])
        name = mega.get("name", f"mega_{mega_idx}")

        # Remplace item1, item2, ... par les blocks de blockList
        for comp in components:
            if comp.get("type") == "patchouli:item":
                item_name = comp.get("item", "")

                # Si c'est itemN
                if item_name.startswith("item"):
                    try:
                        idx = int(item_name[4:]) - 1  # item1 -> index 0
                        if 0 <= idx < len(block_list):
                            comp["item"] = block_list[idx]
                        else:
                            comp["item"] = "minecraft:birch_button"
                    except ValueError:
                        comp["item"] = "minecraft:birch_button"

                # Si c'est recipeN
                elif item_name.startswith("recipe"):
                    try:
                        idx = int(item_name[6:]) - 1  # recipe1 -> index 0
                        if 0 <= idx < len(recipes):
                            comp["item"] = recipes[idx]
                        else:
                            comp["item"] = "minecraft:birch_button"
                    except ValueError:
                        comp["item"] = "minecraft:birch_button"

        out_path = os.path.join(OUT_DIR, f"mega_{name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"Généré: {out_path}")
        mega_idx += 1

if __name__ == "__main__":
    main()