import os

INPUT = "pokopia_data.json"
TEMPLATE = "templates/template_spawn.json"
TEMPLATE_DESTROY = "template_destroy.json"
OUT_DIR = "generated"

def generate_destroy_files(data, template):
    """
    Génère des fichiers JSON pour les Pokémon ayant la capacité 'destroy'.
    Regroupe les Pokémon par 6 (template_destroy.json a 6 slots).
    """
    capacities = data.get("capacities", [])
    destroy_pokemons = [cap for cap in capacities if cap.get("ability") == "destroy"]

    if not destroy_pokemons:
        print("Aucun Pokémon avec la capacité 'destroy' trouvé.")
        return

    file_idx = 1
    # Traiter par groupes de 6
    for i in range(0, len(destroy_pokemons), 6):
        batch = destroy_pokemons[i:i+6]
        out = deepcopy(template)

        # Pour chaque Pokémon du batch (max 6)
        for poke_idx, pokemon in enumerate(batch, start=1):
            poke_name = pokemon.get("name", "")
            blocks = pokemon.get("blocks", [])

            # Remplacer l'image du Pokémon (poke1.png -> poke6.png)
            for comp in out.get("components", []):
                if comp.get("type") == "patchouli:image":
                    image_name = comp.get("image", "")
                    if image_name == f"cobblemonfury:pokesprites/poke{poke_idx}.png":
                        comp["image"] = f"cobblemonfury:pokesprites/{poke_name}.png"

            # Remplacer les items (poke1item1, poke1item2, poke1item3, etc.)
            fill_placeholders(out.get("components", []), f"poke{poke_idx}", blocks)

        # Si moins de 6 Pokémon, remplir les slots restants avec des boutons par défaut
        for poke_idx in range(len(batch) + 1, 7):
            # Masquer l'image en mettant une image transparente ou vide
            for comp in out.get("components", []):
                if comp.get("type") == "patchouli:image":
                    image_name = comp.get("image", "")
                    if image_name == f"cobblemonfury:pokesprites/poke{poke_idx}.png":
                        comp["image"] = "cobblemonfury:pokesprites/0_break.png"

            # Remplir avec des boutons par défaut
            fill_placeholders(out.get("components", []), f"poke{poke_idx}", [])

        # Sauvegarder le fichier
        out_path = os.path.join(OUT_DIR, f"destroy{file_idx}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)

        print(f"Généré (destroy): {out_path}")
        file_idx += 1

    # Générer les fichiers pour les Pokémon avec la capacité "destroy"
    with open(TEMPLATE_DESTROY, "r", encoding="utf-8") as f:
        template_destroy = json.load(f)

    generate_destroy_files(data, template_destroy)
