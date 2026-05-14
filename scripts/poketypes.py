import pandas as pd
from collections import defaultdict

def create_java_sets_by_type_and_strength(excel_file):
    df = pd.read_excel(excel_file, sheet_name='1.7')
    
    # Dictionary: key = type + strength range, value = list of names
    type_strength_to_names = defaultdict(list)
    
    for _, row in df.iterrows():
        type_ = row['type2']
        name = row['name']
        strength = row['kl']
        
        if pd.notna(type_) and pd.notna(name) and pd.notna(strength):
            # Capitalize first letter of Pokémon name
            capitalized_name = name[0].upper() + name[1:]
            
            # Determine strength range
            if strength in [1]:
                strength_suffix = "S"
            elif strength in [2,3]:
                strength_suffix = "M"
            else:
                continue  # Skip other strengths
            
            # Key for dictionary
            key = type_.lower() + strength_suffix
            type_strength_to_names[key].append(capitalized_name)
    
    # Generate Java code
    java_code_lines = []
    for key, names in type_strength_to_names.items():
        # Remove duplicates and sort
        names = sorted(set(names))
        names_list = ",".join(f'"{n}"' for n in names)
        java_line = f"public static final Set<String> {key} = Set.of({names_list});"
        java_code_lines.append(java_line)
    
    java_code = "\n".join(java_code_lines)
    print(java_code)
    return java_code

# Example usage
create_java_sets_by_type_and_strength(r"C:\Users\garat\OneDrive\Music\00modcreator\generatefiles\pokedrop.xlsx")