import pandas as pd
import json
import os
import math


def create_drop_files(excel_file):
    # Lire les données à partir du fichier Excel
    df = pd.read_excel(excel_file,sheet_name='DROPS')

    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        name = row['name'].lower()
        drop = row['drop']
        percentage = row['percentage']
        quantity = row['quantity']

        drop2 = row['drop2']
        percentage2 = row['percentage2']
        quantity2 = row['quantity2']

        if not math.isnan(quantity):
            quantity = int(quantity)
        if not math.isnan(quantity2):
            quantity2 = int(quantity2)

        if percentage != percentage:
            percentage = 100

            amount = 1

        if percentage2 != percentage2:
            percentage2 = 100

        if quantity != quantity:
            entry1 = {
                "item": drop,
                "percentage": percentage + 0.0
            }
        else:
            entry1 = {
                "item": drop,
                "quantityRange": str(quantity) + '-' + str(quantity)
            }
        if drop == drop and drop2 == drop2:
            if quantity2 != quantity2:
                entry2 = {
                    "item": drop2,
                    "percentage": percentage + 0.0}
            else:
                entry2 = {
                    "item": drop2,
                    "quantityRange": str(quantity2) + '-' + str(quantity2)
                }

        if drop == drop and drop2 == drop2:
            amount = 2
            entry1 = entry1, entry2
        else:
            entry1 = [entry1]

        # Créer un dictionnaire avec les données
        data = {
            "target": "cobblemon:" + name,
            "drops": {
                "amount": amount,
                "entries":
                    entry1

            }
        }
        if drop == drop:
            # Créer le nom de fichier
            filename = os.path.join('drop', f"{name}.json")
            print(name)

            # Écrire les données dans un fichier JSON
            with open(filename, "w") as file:
                json.dump(data, file)


def create_spawn_files(excel_file):
    # Lire les données à partir du fichier Excel
    df = pd.read_excel(excel_file)

    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        name = row['name']
        biome = row['biome']

        weight = row['weight']
        if not math.isnan(weight):
            weight = float(row['weight']) + 0.0
        number = int(row['number'])
        if not isinstance(biome, float):
            biomes = biome.split(',')
            spawns = []
            condition = "no"
            for index, biome in enumerate(biomes):
                if biome == "desert":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_sandy"]
                elif biome == "jungle":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_jungle"]
                elif biome == "volcanic":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_volcanic"]
                elif biome == "mountain":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_mountain"]
                elif biome == "forest":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_forest"]
                elif biome == "plains":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_plains"]
                elif biome == "beach":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_beach"]
                elif biome == "cave":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_cave"]
                elif biome == "lush":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_lush"]
                elif biome == "savanna":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_savanna"]
                elif biome == "badlands":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_badlands"]
                elif biome == "snow":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_freezing"]
                # a tester
                elif biome == "cherry":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["minecraft:cherry_grove"]
                elif biome == "swamp":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_swamp"]
                elif biome == "swampsurface":
                    presets = ["water_surface"]
                    context = "surface"
                    biome = ["#cobblemon:is_swamp"]
                elif biome == "flower":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_floral"]
                elif biome == "magical":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_magical"]
                elif biome == "thermal":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_thermal"]
                elif biome == "taiga":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_taiga"]
                elif biome == "mushroom":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_mushroom"]
                elif biome == "nether":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#minecraft:is_nether"]
                elif biome == "end":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#minecraft:is_end"]
                elif biome == "overworld":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_overworld"]
                # attention
                elif biome == "night":
                    presets = ["natural"]
                    context = "grounded"
                    biome = ["#cobblemon:is_overworld"]
                    condition = "night"
                elif biome == "deep":
                    presets = ["underwater"]
                    context = "submerged"
                    biome = ["#cobblemon:is_deep"]
                elif biome == "hot_ocean":
                    presets = ["underwater"]
                    context = "submerged"
                    biome = ["#cobblemon:is_warm_ocean"]
                elif biome == "cold_ocean":
                    presets = ["underwater"]
                    context = "submerged"
                    biome = ["#cobblemon:is_frozen_ocean"]
                elif biome == "river":
                    presets = ["underwater"]
                    context = "submerged"
                    biome = ["#cobblemon:is_river"]
                elif biome == "ocean":
                    presets = ["underwater"]
                    context = "submerged"
                    biome = ["#cobblemon:is_ocean"]
                elif biome == "surface":
                    presets = ["water_surface"]
                    context = "surface"
                    biome = ["#cobblemon:is_ocean"]
                else:
                    print(biome)
                    presets = ["water_surface"]
                    context = "surface"
                    biome = ["WOWO"]

                spawn = {
                    "id": name + "-" + str(index + 1),
                    "pokemon": name,
                    "presets": presets,
                    "type": "pokemon",
                    "context": context,
                    "bucket": "common",
                    "level": "20-44",
                    "weight": weight,
                    "condition": {
                        "minSkyLight": 0,
                        "maxSkyLight": 15,
                        "biomes": biome
                    }
                }
                if condition != "no":
                    spawn["condition"]["timeRange"] = condition
                    # spawn["condition"]["minSkyLight"] = 8
                spawns.append(spawn)

                # Créer un dictionnaire avec les données
            data = {
                "enabled": True,
                "neededInstalledMods": [],
                "neededUninstalledMods": [],
                "spawns": spawns
            }
            if biome == biome:
                # Créer le nom de fichier
                filename = os.path.join('spawn', f"{f"{number:04}" + "_" + name}.json")

                # Écrire les données dans un fichier JSON
                with open(filename, "w") as file:
                    json.dump(data, file)


# def create_ftb_quest(excel_file):
#     # Lire les données à partir du fichier Excel
#     df = pd.read_excel(excel_file)
#
#     # Parcourir les lignes du DataFrame
#     for index, row in df.iterrows():
#         type = row['type']
#         strength = row['strength']
#         name = row['name']
#         group = row['group']
#
#         wa1 = []
#         wa2 = []
#
#         spawn = {
#             "action": "obtain",
#             "entity": "cobblemon:torkoal",
#             "form": "choice_any",
#             "gender": "choice_any",
#             "id": ",
#             "pokemon_type": "choice_any",
#             "region": "choice_any",
#             "shiny": "false",
#             "type": "cobblemon_tasks:cobblemon_task",
#             "value": "1L"
#         }
#
#         # Créer un dictionnaire avec les données
#     data = {
#         "enabled": True,
#         "neededInstalledMods": [],
#         "neededUninstalledMods": [],
#         "spawns": spawn
#     }
#
#     # Créer le nom de fichier
#     # filename = os.path.join('spawn', f"{f"{00000000}" + "_" + name}.json")
#
#     # Écrire les données dans un fichier JSON
#     with open('data.snbt', 'w') as file:
#         file.write(custom_format(data))
#
#
# def custom_format(data):
#     print(data)
#     if data == "1L":
#         print("ok")
#         return "1L"
#     if data == "false":
#         return "false"
#     elif isinstance(data, dict):
#         return '{ ' + ' '.join(f'{k}: {custom_format(v)}' for k, v in data.items()) + ' }'
#     elif isinstance(data, list):
#         return '[ ' + ' '.join(custom_format(i) for i in data) + ' ]'
#     elif isinstance(data, str):
#         return f'"{data}"'
#
#     else:
#         return str(data)

def create_variables(excel_file):
    #     # Lire les données à partir du fichier Excel
    df = pd.read_excel(excel_file,sheet_name='DROPS')
    f1 = ""
    f2 = ""
    s1 = ""
    s2 = ""
    d1 = ""
    d2 = ""
    g1 = ""
    g2 = ""
    p1 = ""
    p2 = ""
    e1 = ""
    e2 = ""
    c1 = ""
    c2 = ""
    n1 = ""
    n2 = ""
    i1 = ""
    i2 = ""
    v1 = ""
    v2 = ""
    
    for index, row in df.iterrows():
        type = row['type']
        strength = row['strength']
        name = row['name']
        if (type == 'F' and (strength == 1.0 or strength == "1")):
            f1 = f1 + name.capitalize() + ','
        if (type == 'F' and strength >= 2.0):
            f2 = f2 + name.capitalize() + ','
        if (type == 'R' and strength == 1.0):
            s1 = s1 + name.capitalize() + ','
        if (type == 'R' and strength >= 2.0):
            s2 = s2 + name.capitalize() + ','
        if (type == 'D' and strength == 1.0):
            d1 = d1 + name.capitalize() + ','
        if (type == 'D' and strength >= 2.0):
            d2 = d2 + name.capitalize() + ','
        if (type == 'G' and strength == 1.0):
            g1 = g1 + name.capitalize() + ','
        if (type == 'G' and strength >= 2.0):
            g2 = g2 + name.capitalize() + ','
        if (type == 'P' and strength == 1.0):
            p1 = p1 + name.capitalize() + ','
        if (type == 'P' and strength >= 2.0):
            p2 = p2 + name.capitalize() + ','
        if (type == 'E' and strength == 1.0):
            e1 = e1 + name.capitalize() + ','
        if (type == 'E' and strength >= 2.0):
            e2 = e2 + name.capitalize() + ','
        if (type == 'C' and strength == 1.0):
            c1 = c1 + name.capitalize() + ','
        if (type == 'C' and strength >= 2.0):
            c2 = c2 + name.capitalize() + ','
        if (type == 'N' and strength == 1.0):
            n1 = n1 + name.capitalize() + ','
        if (type == 'N' and strength >= 2.0):
            n2 = n2 + name.capitalize() + ','
        if (type == 'V' and strength == 1.0):
            v1 = v1 + name.capitalize() + ','
        if (type == 'V' and strength >= 2.0):
            v2 = v2 + name.capitalize() + ','
        if (type == 'I' and strength == 1.0):
            i1 = i1 + name.capitalize() + ','
        if (type == 'I' and strength >= 2.0):
            i2 = i2 + name.capitalize() + ','

    print(f1)
    print("            ")
    print(f2)
    print("            ")
    print(s1)
    print("            ")
    print(s2)
    print("            ")
    print(d1)
    print("            ")
    print(d2)
    print("            ")
    print(g1)
    print("            ")
    print(g2)
    print("            ")
    print(p1)
    print("            ")
    print(p2)
    print("            ")
    print(e1)
    print("            ")
    print(e2)
    print("            ")
    print(c1)
    print("            ")
    print(c2)
    print("            ")
    print(n1)
    print("            ")
    print(n2)
    print("            ")
    print(v1)
    print("            ")
    print(v2)
    print("            ")
    print(i1)
    print("            ")
    print(i2)
    print("            ")


# import os

# def create_icon_files():

# # Define the array with new filenames
#     filenames = [
#     "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise",
#     "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata",
#     "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀",
#     "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales",
#     "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat",
#     "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe",
#     "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp",
#     "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta",
#     "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong",
#     "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby",
#     "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan",
#     "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra",
#     "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir",
#     "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon",
#     "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini",
#     "Dragonair", "Dragonite", "Mewtwo", "Mew", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion",
#     "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak",
#     "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu",
#     "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom",
#     "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow",
#     "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar",
#     "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring",
#     "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory",
#     "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop",
#     "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar",
#     "Tyranitar", "Lugia", "Ho-oh", "Celebi", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken",
#     "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon",
#     "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow",
#     "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom",
#     "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita",
#     "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron",
#     "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin",
#     "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig",
#     "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper",
#     "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily",
#     "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops",
#     "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail",
#     "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock",
#     "Regice", "Registeel", "Latias", "Latios", "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys", "Turtwig",
#     "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia",
#     "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade",
#     "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen", "Pachirisu",
#     "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary",
#     "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong",
#     "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu",
#     "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon",
#     "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth",
#     "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z",
#     "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran",
#     "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus", "Victini", "Snivy",
#     "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog",
#     "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour",
#     "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore",
#     "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole",
#     "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede",
#     "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile",
#     "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask",
#     "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark",
#     "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett",
#     "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier",
#     "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn",
#     "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent",
#     "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk",
#     "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary",
#     "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Volcarona", "Cobalion",
#     "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom", "Landorus", "Kyurem", "Keldeo", "Meloetta",
#     "Genesect", "Chespin", "Quilladin", "Chesnaught", "Fennekin", "Braixen", "Delphox", "Froakie", "Frogadier",
#     "Greninja", "Bunnelby", "Diggersby", "Fletchling", "Fletchinder", "Talonflame", "Scatterbug", "Spewpa", "Vivillon",
#     "Litleo", "Pyroar", "Flabébé", "Floette", "Florges", "Skiddo", "Gogoat", "Pancham", "Pangoro", "Furfrou", "Espurr",
#     "Meowstic", "Honedge", "Doublade", "Aegislash", "Spritzee", "Aromatisse", "Swirlix", "Slurpuff", "Inkay", "Malamar",
#     "Binacle", "Barbaracle", "Skrelp", "Dragalge", "Clauncher", "Clawitzer", "Helioptile", "Heliolisk", "Tyrunt",
#     "Tyrantrum", "Amaura", "Aurorus", "Sylveon", "Hawlucha", "Dedenne", "Carbink", "Goomy", "Sliggoo", "Goodra",
#     "Klefki", "Phantump", "Trevenant", "Pumpkaboo", "Gourgeist", "Bergmite", "Avalugg", "Noibat", "Noivern", "Xerneas",
#     "Yveltal", "Zygarde", "Diancie", "Hoopa", "Volcanion", "Rowlet", "Dartrix", "Decidueye", "Litten", "Torracat",
#     "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos",
#     "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio", "Cutiefly", "Ribombee", "Rockruff",
#     "Lycanroc", "Wishiwashi", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis",
#     "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee",
#     "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku",
#     "Null", "Silvally", "Minior", "Komala", "Turtonator", "Togedemaru", "Mimikyu", "Bruxish", "Drampa",
#     "Dhelmise", "Jangmo-o", "Hakamo-o", "Kommo-o", "Tapu Koko", "Tapu Lele", "Tapu Bulu", "Tapu Fini", "Cosmog",
#     "Cosmoem", "Solgaleo", "Lunala", "Nihilego", "Buzzwole", "Pheromosa", "Xurkitree", "Celesteela", "Kartana",
#     "Guzzlord", "Necrozma", "Magearna", "Marshadow", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Zeraora",
#     "Meltan", "Melmetal", "Grookey", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile",
#     "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle",
#     "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund",
#     "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant",
#     "Arrokuda", "Barraskewda", "Toxel", "Toxtricity", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea",
#     "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker",
#     "Cursola", "Sirfetch'd", "Mr. Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom",
#     "Frosmoth", "Stonjourner", "Eiscue", "Indeedee", "Morpeko", "Cufant", "Copperajah", "Dracozolt", "Arctozolt",
#     "Dracovish", "Arctovish", "Duraludon", "Dreepy", "Drakloak", "Dragapult", "Zacian", "Zamazenta", "Eternatus",
#     "Kubfu", "Urshifu", "Zarude", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Calyrex", "Wyrdeer", "Kleavor",
#     "Ursaluna", "Basculegion", "Sneasler", "Overqwil", "Enamorus", "Sprigatito", "Floragato", "Meowscarada", "Fuecoco",
#     "Crocalor", "Skeledirge", "Quaxly", "Quaxwell", "Quaquaval", "Lechonk", "Oinkologne", "Tarountula", "Spidops",
#     "Nymble", "Lokix", "Pawmi", "Pawmo", "Pawmot", "Tandemaus", "Maushold", "Fidough", "Dachsbun", "Smoliv", "Dolliv",
#     "Arboliva", "Squawkabilly", "Nacli", "Naclstack", "Garganacl", "Charcadet", "Armarouge", "Ceruledge", "Tadbulb",
#     "Bellibolt", "Wattrel", "Kilowattrel", "Maschiff", "Mabosstiff", "Shroodle", "Grafaiai", "Bramblin", "Brambleghast",
#     "Toedscool", "Toedscruel", "Klawf", "Capsakid", "Scovillain", "Rellor", "Rabsca", "Flittle", "Espathra",
#     "Tinkatink", "Tinkatuff", "Tinkaton", "Wiglett", "Wugtrio", "Bombirdier", "Finizen", "Palafin", "Varoom",
#     "Revavroom", "Cyclizar", "Orthworm", "Glimmet", "Glimmora", "Greavard", "Houndstone", "Flamigo", "Cetoddle",
#     "Cetitan", "Veluza", "Dondozo", "Tatsugiri", "Annihilape", "Clodsire", "Farigiraf", "Dudunsparce", "Kingambit",
#     "Great Tusk", "Scream Tail", "Brute Bonnet", "Flutter Mane", "Slither Wing", "Sandy Shocks", "Iron Treads",
#     "Iron Bundle", "Iron Hands", "Iron Jugulis", "Iron Moth", "Iron Thorns", "Frigibax", "Arctibax", "Baxcalibur",
#     "Gimmighoul", "Gholdengo", "Wo-Chien", "Chien-Pao", "Ting-Lu", "Chi-Yu", "Roaring Moon", "Iron Valiant", "Koraidon",
#     "Miraidon", "Walking Wake", "Iron Leaves", "Dipplin", "Poltchageist", "Sinistcha", "Okidogi", "Munkidori",
#     "Fezandipiti", "Ogerpon", "Archaludon", "Hydrapple", "Gouging Fire", "Raging Bolt", "Iron Boulder", "Iron Crown",
#     "Terapagos", "Pecharunt"
#    ]

    # # Directory containing the files
    # directory = "pokesprites/"

    # # Iterate through the files and rename them
    # for i in range(1, len(filenames) + 1):

    #     old_name = f"{filenames[i]}"
    #     # new_name = filenames[i][0].lower() + filenames[i][1:]
    #     old_path = os.path.join(directory, old_name + ".png")
    #     print(f"{old_path}")
    #     # new_path = os.path.join(directory, new_name + ".png")

    #     # # Rename the file
    #     # os.rename(old_path, new_path)
    #     # print(f"Renamed {old_path} to {new_path}")

import os

import os

def rename_files_to_png(directory):
    for filename in os.listdir(directory):
        # Check if the file is not a PNG
        if not filename.lower().endswith('.png'):
            new_name = os.path.splitext(filename)[0] + '.png'  # Change the extension to .png
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))
            print(f'Renamed: {filename} to {new_name}')

# Provide the path to the directory containing the files
directory_path = 'path_to_your_directory'

#srename_files_to_png('pokesprites/')

#rename_files()



# Appel de la fonction avec le nom du fichier Excel erreur sur la dernier ligne, pas grave
create_drop_files("pokedrop.xlsx")
# create_spawn_files("pokedrop.xlsx")
#create_variables("pokedrop.xlsx")

#create_icon_files()
