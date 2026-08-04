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
TEMPLATE_ENTRY = "templates/template_entry.json"
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

    with open(TEMPLATE_ENTRY, "r", encoding="utf-8") as f:
        template_entry = json.load(f)

    # ---------------------------------------------------------
    # Récupération des données
    # ---------------------------------------------------------
    habitats = data.get("habitats", [])
    capacities = data.get("capacities", [])
    mega_habitats = data.get("mega_habitats", [])

    # ---------------------------------------------------------
    # Génération des Entries par Megahabitat
    # ---------------------------------------------------------
    for mega in mega_habitats:
        mega_name = mega.get("name", "unknown")
        mega_pokemons = mega.get("pokemons", [])
        rotom = mega.get("rotom", "")

        # Sauter les megahabitats vides (sans recettes et sans pokémons)
        if not mega.get("recipes") and not mega_pokemons:
            continue

        # Créer des dictionnaires pour retrouver habitats et capacités
        habitat_dict = {h.get("name"): h for h in habitats}
        capacity_dict = {c.get("name"): c for c in capacities}

        # Filtrer les habitats et capacités pour ce megahabitat
        mega_habitats_list = [habitat_dict.get(poke) for poke in mega_pokemons if poke in habitat_dict and habitat_dict.get(poke).get("hab")]
        mega_capacities_destroy = [capacity_dict.get(poke) for poke in mega_pokemons if poke in capacity_dict and capacity_dict.get(poke).get("ability") == "destroy"]
        mega_capacities_transform = [capacity_dict.get(poke) for poke in mega_pokemons if poke in capacity_dict and capacity_dict.get(poke).get("ability") == "transform"]

        # Générer la page du megahabitat
        all_pages = []
        mega_page = deepcopy(template_mega_habitat)
        components = mega_page.get("components", [])

        recipes = mega.get("recipes", [])
        pokemons = mega.get("pokemons", [])

        # Remplacer les recettes (recipeN_ingredientM et recipeN_result)
        for comp in components:
            if comp.get("type") == "patchouli:item":
                item_name = comp.get("item", "")

                # Si c'est recipeN_ingredientM (ex: recipe1_ingredient2)
                if item_name.startswith("recipe") and "_ingredient" in item_name:
                    try:
                        # Extraire le numéro de recette et d'ingrédient
                        # Format: recipeN_ingredientM
                        parts = item_name.replace("recipe", "").split("_ingredient")
                        recipe_idx = int(parts[0]) - 1  # recipe1 -> index 0
                        ingredient_idx = int(parts[1]) - 1  # ingredient1 -> index 0

                        if 0 <= recipe_idx < len(recipes):
                            ingredients = recipes[recipe_idx].get("ingredients", [])
                            if 0 <= ingredient_idx < len(ingredients):
                                comp["item"] = ingredients[ingredient_idx]
                            else:
                                comp["item"] = "minecraft:air"
                        else:
                            comp["item"] = "minecraft:air"
                    except (ValueError, IndexError):
                        comp["item"] = "minecraft:air"

                # Si c'est recipeN_result (ex: recipe1_result)
                elif item_name.startswith("recipe") and "_result" in item_name:
                    try:
                        # Format: recipeN_result
                        recipe_num = item_name.replace("recipe", "").replace("_result", "")
                        recipe_idx = int(recipe_num) - 1  # recipe1 -> index 0

                        if 0 <= recipe_idx < len(recipes):
                            result = recipes[recipe_idx].get("result", "minecraft:air")
                            comp["item"] = result
                        else:
                            comp["item"] = "minecraft:air"
                    except (ValueError, IndexError):
                        comp["item"] = "minecraft:air"

        # Remplacer les images des pokémons (poke1.png à poke6.png)
        for comp in components:
            if comp.get("type") == "patchouli:image":
                image_name = comp.get("image", "")

                for poke_idx in range(1, 7):
                    if f"/poke{poke_idx}.png" in image_name:
                        if poke_idx - 1 < len(pokemons):
                            poke_name = pokemons[poke_idx - 1]
                            comp["image"] = f"cobblemonfury:pokesprites/{poke_name}.png"
                        else:
                            # Pas de pokémon pour ce slot, on supprime l'image
                            comp["image"] = ""
                        break

        # Filtrer les composants vides (items air et images vides)
        components = [
            comp for comp in components
            if not (comp.get("item") == "minecraft:air" or (comp.get("type") == "patchouli:image" and comp.get("image") == ""))
        ]
        mega_page["components"] = components

        mega_page_name = f"{mega_name}_mega"
        mega_page_path = os.path.join(OUT_DIR, f"{mega_page_name}.json")
        with open(mega_page_path, "w", encoding="utf-8") as f:
            json.dump(mega_page, f, ensure_ascii=False, indent=2)
        print(f"Généré: {mega_page_path}")
        all_pages.append({"type": f"cobblemonfury:{mega_page_name}"})

        # Générer les pages d'habitats
        hab_pages = []
        hab_page_idx = 1
        for i in range(0, len(mega_habitats_list), 2):
            h1 = mega_habitats_list[i]
            h2 = mega_habitats_list[i + 1] if i + 1 < len(mega_habitats_list) else None

            out = deepcopy(template_hab)
            items1 = h1.get("hab", []) or []
            name1 = h1.get("name", f"hab_{i}")

            fill_placeholders(out.get("components", []), "poke1", items1)

            if h2:
                items2 = h2.get("hab", []) or []
                name2 = h2.get("name", f"hab_{i+1}")
                fill_placeholders(out.get("components", []), "poke2", items2)

                for comp in out.get("components", []):
                    if comp.get("type") == "patchouli:image":
                        x = comp.get("x")
                        y = comp.get("y")
                        if x == 60 and y == 5:
                            comp["image"] = f"cobblemonfury:pokesprites/{name1}.png"
                        elif x == 60 and y == 80:
                            comp["image"] = f"cobblemonfury:pokesprites/{name2}.png"
            else:
                fill_placeholders(out.get("components", []), "poke2", [])
                for comp in out.get("components", []):
                    if comp.get("type") == "patchouli:image":
                        x = comp.get("x")
                        y = comp.get("y")
                        if x == 60 and y == 5:
                            comp["image"] = f"cobblemonfury:pokesprites/{name1}.png"

            page_name = f"{mega_name}_hab_{hab_page_idx}"
            out_path = os.path.join(OUT_DIR, f"{page_name}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"Généré: {out_path}")
            hab_pages.append({"type": f"cobblemonfury:{page_name}"})
            hab_page_idx += 1

        # Générer les pages de capacités destroy
        capa_pages = []
        capa_page_idx = 1
        for i in range(0, len(mega_capacities_destroy), 6):
            chunk = mega_capacities_destroy[i:i+6]
            pokemon_list = [{"name": cap.get("name"), "items_to_display": cap.get("blocks", [])} for cap in chunk]

            out = deepcopy(template_destroy)
            components = out.get("components", [])

            for slot_idx in range(1, 7):
                prefix = f"poke{slot_idx}"
                if slot_idx - 1 < len(pokemon_list):
                    poke = pokemon_list[slot_idx - 1]
                    name = poke.get("name", f"unknown_{slot_idx}")
                    items = poke.get("items_to_display", [])
                    fill_placeholders(components, prefix, items, fallback=None)
                    for comp in components:
                        if comp.get("type") == "patchouli:image":
                            if f"pokesprites/{prefix}.png" in comp.get("image", ""):
                                comp["image"] = f"cobblemonfury:pokesprites/{name}.png"
                else:
                    fill_placeholders(components, prefix, [], fallback=None)
                    components = [
                        comp for comp in components
                        if not (comp.get("type") == "patchouli:image" and f"pokesprites/{prefix}.png" in comp.get("image", ""))
                    ]

            out["components"] = components
            page_name = f"{mega_name}_capa_{capa_page_idx}"
            out_path = os.path.join(OUT_DIR, f"{page_name}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"Généré: {out_path}")
            capa_pages.append({"type": f"cobblemonfury:{page_name}"})
            capa_page_idx += 1

        # Générer les pages de capacités transform
        for i in range(0, len(mega_capacities_transform), 6):
            chunk = mega_capacities_transform[i:i+6]
            pokemon_list = [{"name": cap.get("name"), "items_to_display": cap.get("blocks", [])} for cap in chunk]

            out = deepcopy(template_transform)
            components = out.get("components", [])

            for slot_idx in range(1, 7):
                prefix = f"poke{slot_idx}"
                if slot_idx - 1 < len(pokemon_list):
                    poke = pokemon_list[slot_idx - 1]
                    name = poke.get("name", f"unknown_{slot_idx}")
                    items = poke.get("items_to_display", [])
                    fill_placeholders(components, prefix, items, fallback=None)
                    for comp in components:
                        if comp.get("type") == "patchouli:image":
                            if f"pokesprites/{prefix}.png" in comp.get("image", ""):
                                comp["image"] = f"cobblemonfury:pokesprites/{name}.png"
                else:
                    fill_placeholders(components, prefix, [], fallback=None)
                    components = [
                        comp for comp in components
                        if not (comp.get("type") == "patchouli:image" and f"pokesprites/{prefix}.png" in comp.get("image", ""))
                    ]

            out["components"] = components
            page_name = f"{mega_name}_capa_{capa_page_idx}"
            out_path = os.path.join(OUT_DIR, f"{page_name}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"Généré: {out_path}")
            capa_pages.append({"type": f"cobblemonfury:{page_name}"})
            capa_page_idx += 1

        # Créer le fichier entry pour ce megahabitat
        entry = deepcopy(template_entry)
        entry["name"] = mega_name
        entry["icon"] = rotom if rotom else "minecraft:book"
        entry["pages"] = all_pages + hab_pages + capa_pages

        entry_path = os.path.join(OUT_DIR, f"entry_{mega_name}.json")
        with open(entry_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
        print(f"Généré entry: {entry_path}")

if __name__ == "__main__":
    main()