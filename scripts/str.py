import os
import math
from nbtlib import File, Compound, List, ByteArray, Short, Int


def split_custom_schem_v3(input_file, chunk_size, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    schem_file = File.load(input_file, gzipped=True)
    root = schem_file["Schematic"]

    if root["Version"] != 3:
        raise ValueError("Unsupported schematic version")

    width = root["Width"]
    height = root["Height"]
    length = root["Length"]

    palette = root["Blocks"]["Palette"]
    palette_inv = {v: k for k, v in palette.items()}
    block_data = root["Blocks"]["Data"]
    total_blocks = width * height * length

    def idx(x, y, z):
        return x + z * width + y * width * length

    # if len(block_data) != total_blocks:
    #     raise ValueError("BlockData length mismatch")

    chunks_x = math.ceil(width / chunk_size)
    chunks_y = math.ceil(height / chunk_size)
    chunks_z = math.ceil(length / chunk_size)

    for cx in range(chunks_x):
        for cy in range(chunks_y):
            for cz in range(chunks_z):
                c_width = min(chunk_size, width - cx * chunk_size)
                c_height = min(chunk_size, height - cy * chunk_size)
                c_length = min(chunk_size, length - cz * chunk_size)

                chunk_block_ids = []
                local_palette = {}
                local_palette_rev = []
                next_id = 0

                for y in range(c_height):
                    for z in range(c_length):
                        for x in range(c_width):
                            gx = cx * chunk_size + x
                            gy = cy * chunk_size + y
                            gz = cz * chunk_size + z
                            global_id = int(block_data[idx(gx, gy, gz)]) & 0xFF
                            if global_id not in local_palette:
                                local_palette[global_id] = next_id
                                local_palette_rev.append(global_id)
                                next_id += 1
                            chunk_block_ids.append(local_palette[global_id])

                chunk_palette = Compound()
                for local_id, global_id in enumerate(local_palette_rev):
                    block_name = palette_inv[global_id]
                    chunk_palette[block_name] = Int(local_id)

                chunk_block_data = ByteArray(chunk_block_ids)

                chunk_root = Compound({
                    "Schematic": Compound({
                        "Version": Int(3),
                        "Width": Short(c_width),
                        "Height": Short(c_height),
                        "Length": Short(c_length),
                        "Blocks": Compound({
                            "Palette": chunk_palette,
                            "Data": chunk_block_data,
                            "BlockEntities": List([]),
                        }),
                        "Biomes": root["Biomes"],  # You can also split biomes per chunk if needed
                        "Metadata": root.get("Metadata", Compound()),
                        "Offset": root.get("Offset", List([Int(0), Int(0), Int(0)])),
                        "DataVersion": root["DataVersion"]
                    })
                })

                chunk_file = File(chunk_root)
                filename = f"chunk_{cx}_{cy}_{cz}.schem"
                filepath = os.path.join(output_dir, filename)
                chunk_file.save(filepath, gzipped=True)

                print(f"Saved {filename} ({c_width}x{c_height}x{c_length})")

    print("✅ Done splitting.")


# Exemple d'utilisation :
split_custom_schem_v3("source.schem", 128, "output_chunks_final_128")
