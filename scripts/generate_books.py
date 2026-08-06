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
TEMPLATE_STARDUST = "templates/template_stardust.json"
OUT_DIR = "generated"

# Liste des évolutions pokémon
EVOLUTIONS = {
    "bulbasaur": ["ivysaur", "venusaur"],
    "charmander": ["charmeleon", "charizard"],
    "squirtle": ["wartortle", "blastoise"],
    "caterpie": ["metapod", "butterfree"],
    "weedle": ["kakuna", "beedrill"],
    "pidgey": ["pidgeotto", "pidgeot"],
    "rattata": ["raticate"],
    "spearow": ["fearow"],
    "ekans": ["arbok"],
    "pikachu": ["raichu"],
    "sandshrew": ["sandslash"],
    "nidoranf": ["nidorina", "nidoqueen"],
    "nidoranm": ["nidorino", "nidoking"],
    "clefairy": ["clefable"],
    "vulpix": ["ninetales"],
    "jigglypuff": ["wigglytuff"],
    "zubat": ["golbat", "crobat"],
    "oddish": ["gloom", "vileplume", "bellossom"],
    "paras": ["parasect"],
    "venonat": ["venomoth"],
    "diglett": ["dugtrio"],
    "meowth": ["persian"],
    "psyduck": ["golduck"],
    "mankey": ["primeape", "annihilape"],
    "growlithe": ["arcanine"],
    "poliwag": ["poliwhirl", "poliwrath", "politoed"],
    "abra": ["kadabra", "alakazam"],
    "machop": ["machoke", "machamp"],
    "bellsprout": ["weepinbell", "victreebel"],
    "tentacool": ["tentacruel"],
    "geodude": ["graveler", "golem"],
    "ponyta": ["rapidash"],
    "slowpoke": ["slowbro", "slowking"],
    "magnemite": ["magneton", "magnezone"],
    "farfetchd": ["sirfetchd"],
    "doduo": ["dodrio"],
    "seel": ["dewgong"],
    "grimer": ["muk"],
    "shellder": ["cloyster"],
    "gastly": ["haunter", "gengar"],
    "onix": ["steelix"],
    "drowzee": ["hypno"],
    "krabby": ["kingler"],
    "voltorb": ["electrode"],
    "exeggcute": ["exeggutor"],
    "cubone": ["marowak"],
    "lickitung": ["lickilicky"],
    "koffing": ["weezing"],
    "rhyhorn": ["rhydon", "rhyperior"],
    "chansey": ["blissey"],
    "tangela": ["tangrowth"],
    "horsea": ["seadra", "kingdra"],
    "goldeen": ["seaking"],
    "staryu": ["starmie"],
    "magikarp": ["gyarados"],
    "eevee": ["vaporeon", "jolteon", "flareon", "espeon", "umbreon", "leafeon", "glaceon", "sylveon"],
    "omanyte": ["omastar"],
    "kabuto": ["kabutops"],
    "dratini": ["dragonair", "dragonite"],
    "chikorita": ["bayleef", "meganium"],
    "cyndaquil": ["quilava", "typhlosion"],
    "totodile": ["croconaw", "feraligatr"],
    "sentret": ["furret"],
    "hoothoot": ["noctowl"],
    "ledyba": ["ledian"],
    "spinarak": ["ariados"],
    "chinchou": ["lanturn"],
    "pichu": ["pikachu", "raichu"],
    "cleffa": ["clefairy", "clefable"],
    "igglybuff": ["jigglypuff", "wigglytuff"],
    "togepi": ["togetic", "togekiss"],
    "natu": ["xatu"],
    "mareep": ["flaaffy", "ampharos"],
    "marill": ["azumarill"],
    "hoppip": ["skiploom", "jumpluff"],
    "aipom": ["ambipom"],
    "sunkern": ["sunflora"],
    "yanma": ["yanmega"],
    "wooper": ["quagsire"],
    "murkrow": ["honchkrow"],
    "misdreavus": ["mismagius"],
    "girafarig": ["farigiraf"],
    "pineco": ["forretress"],
    "dunsparce": ["dudunsparce"],
    "gligar": ["gliscor"],
    "snubbull": ["granbull"],
    "sneasel": ["weavile"],
    "teddiursa": ["ursaring"],
    "slugma": ["magcargo"],
    "swinub": ["piloswine", "mamoswine"],
    "corsola": ["cursola"],
    "remoraid": ["octillery"],
    "houndour": ["houndoom"],
    "phanpy": ["donphan"],
    "stantler": ["wyrdeer"],
    "tyrogue": ["hitmonlee", "hitmonchan", "hitmontop"],
    "smoochum": ["jynx"],
    "elekid": ["electabuzz", "electivire"],
    "magby": ["magmar", "magmortar"],
    "larvitar": ["pupitar", "tyranitar"],
    "treecko": ["grovyle", "sceptile"],
    "torchic": ["combusken", "blaziken"],
    "mudkip": ["marshtomp", "swampert"],
    "poochyena": ["mightyena"],
    "zigzagoon": ["linoone"],
    "wurmple": ["silcoon", "beautifly", "cascoon", "dustox"],
    "lotad": ["lombre", "ludicolo"],
    "seedot": ["nuzleaf", "shiftry"],
    "taillow": ["swellow"],
    "wingull": ["pelipper"],
    "ralts": ["kirlia", "gardevoir", "gallade"],
    "surskit": ["masquerain"],
    "shroomish": ["breloom"],
    "slakoth": ["vigoroth", "slaking"],
    "nincada": ["ninjask", "shedinja"],
    "whismur": ["loudred", "exploud"],
    "makuhita": ["hariyama"],
    "azurill": ["marill", "azumarill"],
    "nosepass": ["probopass"],
    "skitty": ["delcatty"],
    "aron": ["lairon", "aggron"],
    "meditite": ["medicham"],
    "electrike": ["manectric"],
    "roselia": ["roserade"],
    "gulpin": ["swalot"],
    "carvanha": ["sharpedo"],
    "wailmer": ["wailord"],
    "numel": ["camerupt"],
    "spoink": ["grumpig"],
    "trapinch": ["vibrava", "flygon"],
    "cacnea": ["cacturne"],
    "swablu": ["altaria"],
    "barboach": ["whiscash"],
    "corphish": ["crawdaunt"],
    "baltoy": ["claydol"],
    "lileep": ["cradily"],
    "anorith": ["armaldo"],
    "feebas": ["milotic"],
    "shuppet": ["banette"],
    "duskull": ["dusclops", "dusknoir"],
    "wynaut": ["wobbuffet"],
    "snorunt": ["glalie", "froslass"],
    "spheal": ["sealeo", "walrein"],
    "clamperl": ["huntail", "gorebyss"],
    "bagon": ["shelgon", "salamence"],
    "beldum": ["metang", "metagross"],
    "turtwig": ["grotle", "torterra"],
    "chimchar": ["monferno", "infernape"],
    "piplup": ["prinplup", "empoleon"],
    "starly": ["staravia", "staraptor"],
    "bidoof": ["bibarel"],
    "kricketot": ["kricketune"],
    "shinx": ["luxio", "luxray"],
    "cranidos": ["rampardos"],
    "shieldon": ["bastiodon"],
    "burmy": ["wormadam", "mothim"],
    "combee": ["vespiquen"],
    "buizel": ["floatzel"],
    "cherubi": ["cherrim"],
    "shellos": ["gastrodon"],
    "drifloon": ["drifblim"],
    "buneary": ["lopunny"],
    "glameow": ["purugly"],
    "chingling": ["chimecho"],
    "stunky": ["skuntank"],
    "bronzor": ["bronzong"],
    "bonsly": ["sudowoodo"],
    "mimejr": ["mrmime"],
    "happiny": ["chansey", "blissey"],
    "gible": ["gabite", "garchomp"],
    "munchlax": ["snorlax"],
    "riolu": ["lucario"],
    "hippopotas": ["hippowdon"],
    "skorupi": ["drapion"],
    "croagunk": ["toxicroak"],
    "finneon": ["lumineon"],
    "mantyke": ["mantine"],
    "snover": ["abomasnow"],
    "oshawott": ["dewott", "samurott"],
    "tepig": ["pignite", "emboar"],
    "snivy": ["servine", "serperior"],
    "patrat": ["watchog"],
    "lillipup": ["herdier", "stoutland"],
    "purrloin": ["liepard"],
    "pansage": ["simisage"],
    "pansear": ["simisear"],
    "panpour": ["simipour"],
    "munna": ["musharna"],
    "pidove": ["tranquill", "unfezant"],
    "blitzle": ["zebstrika"],
    "roggenrola": ["boldore", "gigalith"],
    "woobat": ["swoobat"],
    "drilbur": ["excadrill"],
    "timburr": ["gurdurr", "conkeldurr"],
    "tympole": ["palpitoad", "seismitoad"],
    "sewaddle": ["swadloon", "leavanny"],
    "venipede": ["whirlipede", "scolipede"],
    "cottonee": ["whimsicott"],
    "petilil": ["lilligant"],
    "sandile": ["krokorok", "krookodile"],
    "darumaka": ["darmanitan"],
    "dwebble": ["crustle"],
    "scraggy": ["scrafty"],
    "yamask": ["cofagrigus"],
    "tirtouga": ["carracosta"],
    "archen": ["archeops"],
    "trubbish": ["garbodor"],
    "zorua": ["zoroark"],
    "minccino": ["cinccino"],
    "gothita": ["gothorita", "gothitelle"],
    "solosis": ["duosion", "reuniclus"],
    "ducklett": ["swanna"],
    "vanillite": ["vanillish", "vanilluxe"],
    "deerling": ["sawsbuck"],
    "karrablast": ["escavalier"],
    "foongus": ["amoonguss"],
    "frillish": ["jellicent"],
    "joltik": ["galvantula"],
    "ferroseed": ["ferrothorn"],
    "klink": ["klang", "klinklang"],
    "tynamo": ["eelektrik", "eelektross"],
    "elgyem": ["beheeyem"],
    "litwick": ["lampent", "chandelure"],
    "axew": ["fraxure", "haxorus"],
    "cubchoo": ["beartic"],
    "shelmet": ["accelgor"],
    "mienfoo": ["mienshao"],
    "golett": ["golurk"],
    "pawniard": ["bisharp", "kingambit"],
    "rufflet": ["braviary"],
    "vullaby": ["mandibuzz"],
    "deino": ["zweilous", "hydreigon"],
    "larvesta": ["volcarona"],
    "chespin": ["quilladin", "chesnaught"],
    "fennekin": ["braixen", "delphox"],
    "froakie": ["frogadier", "greninja"],
    "bunnelby": ["diggersby"],
    "fletchling": ["fletchinder", "talonflame"],
    "scatterbug": ["spewpa", "vivillon"],
    "litleo": ["pyroar"],
    "flabebe": ["floette", "florges"],
    "skiddo": ["gogoat"],
    "pancham": ["pangoro"],
    "espurr": ["meowstic"],
    "honedge": ["doublade", "aegislash"],
    "spritzee": ["aromatisse"],
    "swirlix": ["slurpuff"],
    "inkay": ["malamar"],
    "binacle": ["barbaracle"],
    "skrelp": ["dragalge"],
    "clauncher": ["clawitzer"],
    "helioptile": ["heliolisk"],
    "tyrunt": ["tyrantrum"],
    "amaura": ["aurorus"],
    "goomy": ["sliggoo", "goodra"],
    "phantump": ["trevenant"],
    "pumpkaboo": ["gourgeist"],
    "bergmite": ["avalugg"],
    "noibat": ["noivern"],
    "rowlet": ["dartrix", "decidueye"],
    "litten": ["torracat", "incineroar"],
    "popplio": ["brionne", "primarina"],
    "pikipek": ["trumbeak", "toucannon"],
    "yungoos": ["gumshoos"],
    "grubbin": ["charjabug", "vikavolt"],
    "crabrawler": ["crabominable"],
    "cutiefly": ["ribombee"],
    "rockruff": ["lycanroc"],
    "mareanie": ["toxapex"],
    "mudbray": ["mudsdale"],
    "dewpider": ["araquanid"],
    "fomantis": ["lurantis"],
    "morelull": ["shiinotic"],
    "salandit": ["salazzle"],
    "stufful": ["bewear"],
    "bounsweet": ["steenee", "tsareena"],
    "wimpod": ["golisopod"],
    "sandygast": ["palossand"],
    "typenull": ["silvally"],
    "jangmoo": ["hakamooo", "kommoo"],
    "grookey": ["thwackey", "rillaboom"],
    "scorbunny": ["raboot", "cinderace"],
    "sobble": ["drizzile", "inteleon"],
    "skwovet": ["greedent"],
    "rookidee": ["corvisquire", "corviknight"],
    "blipbug": ["dottler", "orbeetle"],
    "nickit": ["thievul"],
    "gossifleur": ["eldegoss"],
    "wooloo": ["dubwool"],
    "chewtle": ["drednaw"],
    "yamper": ["boltund"],
    "rolycoly": ["carkol", "coalossal"],
    "applin": ["flapple", "appletun"],
    "silicobra": ["sandaconda"],
    "arrokuda": ["barraskewda"],
    "toxel": ["toxtricity"],
    "sizzlipede": ["centiskorch"],
    "clobbopus": ["grapploct"],
    "sinistea": ["polteageist"],
    "hatenna": ["hattrem", "hatterene"],
    "impidimp": ["morgrem", "grimmsnarl"],
    "milcery": ["alcremie"],
    "snom": ["frosmoth"],
    "cufant": ["copperajah"],
    "duraludon": ["archaludon"],
    "dreepy": ["drakloak", "dragapult"],
    "sprigatito": ["floragato", "meowscarada"],
    "fuecoco": ["crocalor", "skeledirge"],
    "quaxly": ["quaxwell", "quaquaval"],
    "lechonk": ["oinkologne"],
    "tarountula": ["spidops"],
    "nymble": ["lokix"],
    "pawmi": ["pawmo", "pawmot"],
    "tandemaus": ["maushold"],
    "fidough": ["dachsbun"],
    "smoliv": ["dolliv", "arboliva"],
    "nacli": ["naclstack", "garganacl"],
    "charcadet": ["armarouge", "ceruledge"],
    "tadbulb": ["bellibolt"],
    "wattrel": ["kilowattrel"],
    "maschiff": ["mabosstiff"],
    "shroodle": ["grafaiai"],
    "bramblin": ["brambleghast"],
    "toedscool": ["toedscruel"],
    "capsakid": ["scovillain"],
    "rellor": ["rabsca"],
    "flittle": ["espathra"],
    "tinkatink": ["tinkatuff", "tinkaton"],
    "wiglett": ["wugtrio"],
    "finizen": ["palafin"],
    "varoom": ["revavroom"],
    "glimmet": ["glimmora"],
    "greavard": ["houndstone"],
    "cetoddle": ["cetitan"],
    "frigibax": ["arctibax", "baxcalibur"],
    "gimmighoul": ["gholdengo"],
    "poltchageist": ["sinistcha"]
}

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

    with open(TEMPLATE_STARDUST, "r", encoding="utf-8") as f:
        template_stardust = json.load(f)

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

        # Construire une liste étendue des pokémons incluant les évolutions
        extended_pokemons = list(mega_pokemons)
        for poke in mega_pokemons:
            if poke in habitat_dict and habitat_dict[poke].get("hab"):
                evolutions = EVOLUTIONS.get(poke, [])
                extended_pokemons.extend(evolutions)

        mega_capacities_destroy = [capacity_dict.get(poke) for poke in extended_pokemons if poke in capacity_dict and capacity_dict.get(poke).get("ability") == "destroy"]
        mega_capacities_transform = [capacity_dict.get(poke) for poke in extended_pokemons if poke in capacity_dict and capacity_dict.get(poke).get("ability") == "transform"]
        mega_capacities_stardust = [capacity_dict.get(poke) for poke in extended_pokemons if poke in capacity_dict and capacity_dict.get(poke).get("ability") == "stardust"]

        # On ne génère plus la page du megahabitat
        all_pages = []
        recipes = mega.get("recipes", [])

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

        # Générer les pages de capacités stardust
        for i in range(0, len(mega_capacities_stardust), 6):
            chunk = mega_capacities_stardust[i:i+6]

            out = deepcopy(template_stardust)
            components = out.get("components", [])

            for slot_idx in range(1, 7):
                prefix = f"poke{slot_idx}"
                if slot_idx - 1 < len(chunk):
                    cap = chunk[slot_idx - 1]
                    name = cap.get("name", f"unknown_{slot_idx}")
                    blocks = cap.get("blocks", [])
                    item_price = cap.get("itemPrice", 1)
                    max_value = cap.get("maxValue", 1)

                    # Remplacer les items (poke1item1, poke1item2)
                    fill_placeholders(components, prefix, blocks, fallback=None)

                    # Remplacer l'image
                    for comp in components:
                        if comp.get("type") == "patchouli:image":
                            if f"pokesprites/{prefix}.png" in comp.get("image", ""):
                                comp["image"] = f"cobblemonfury:pokesprites/{name}.png"

                    # Remplacer les textes (poke1price, poke1maxValue)
                    for comp in components:
                        if comp.get("type") == "patchouli:text":
                            text_value = comp.get("text", "")
                            if text_value == f"{prefix}price":
                                comp["text"] = str(item_price)
                            elif text_value == f"{prefix}maxValue":
                                comp["text"] = str(max_value)
                else:
                    # Pas de pokémon pour ce slot, on supprime les composants
                    fill_placeholders(components, prefix, [], fallback=None)
                    components = [
                        comp for comp in components
                        if not (
                            (comp.get("type") == "patchouli:image" and f"pokesprites/{prefix}.png" in comp.get("image", ""))
                            or (comp.get("type") == "patchouli:text" and comp.get("text", "") in [f"{prefix}price", f"{prefix}maxValue"])
                        )
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

        # L'icône est le result de la première recette
        if recipes and len(recipes) > 0:
            entry["icon"] = recipes[0].get("result", "minecraft:book")
        else:
            entry["icon"] = "minecraft:book"

        entry["pages"] = all_pages + hab_pages + capa_pages

        entry_path = os.path.join(OUT_DIR, f"entry_{mega_name}.json")
        with open(entry_path, "w", encoding="utf-8") as f:
            json.dump(entry, f, ensure_ascii=False, indent=2)
        print(f"Généré entry: {entry_path}")

if __name__ == "__main__":
    main()