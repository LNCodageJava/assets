import pandas as pd
import json
import os
import math

def create_spawn_files(excel_file):
    # Lire les données à partir du fichier Excel
    df = pd.read_excel(excel_file)
    
    # Parcourir les lignes du DataFrame
    for index, row in df.iterrows():
        name = row['name']
        biome = row['biome']
        weight = int(row['weight'])+0.0
        number = int(row['number'])

        if biome == "ocean":
          presets = ["underwater"]
          context = "submerged"
          biome = ["#cobblemon:is_ocean", "#cobblemon:is_deep_ocean"]
        else:
          presets = ["natural"]
          context = "grounded"
          biome = [biome]
        
        # Créer un dictionnaire avec les données
        data = {
  "enabled": True,
  "neededInstalledMods": [],
  "neededUninstalledMods": [],
  "spawns": [
    {
      "id": name+"-1",
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
  ]
}
        if biome == biome:
        # Créer le nom de fichier
          filename = os.path.join('spawn', f"{f"{number:04}"+"_"+name}.json")
          print(name)
        
        # Écrire les données dans un fichier JSON
          with open(filename, "w") as file:
              json.dump(data, file)


create_spawn_files("pokedrop.xlsx")
