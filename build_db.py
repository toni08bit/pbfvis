import struct
import os
import time
import osmium
import osmium.osm

import modules.calc_2d as calc_2d
import modules.map_compressor as map_compressor
from values import config

# Check
if (__name__ != "__main__"):
    raise RuntimeError("This is not a module.")
if (os.path.exists(f"{config['database']}/nodes.bin")):
    raise FileExistsError("nodes.bin already exists")

# Initialization
print("[INFO] Opening file.")
file_processor = osmium.FileProcessor(config["target"])
nodes_file = open(f"{config['database']}/nodes.bin","ab")
print("[INFO] Starting.")
start_time = time.time()
last_class = None

# Iteration
for obj in file_processor:
    current_class = obj.__class__
    if (last_class != current_class):
        print(f"[INFO] Processing class: {current_class.__name__}.")
        if (last_class == osmium.osm.Node):
            nodes_file.close()
        last_class = current_class

    tags = dict(obj.tags)    
    if (current_class == osmium.osm.Node):
        # ID
        nodes_file.write(struct.pack("!Q",obj.id))
        # Lat + Lon
        nodes_file.write(struct.pack("!i",round(obj.lat * (10 ** 7))) + struct.pack("!i",round(obj.lon * (10 ** 7))))
        # Tags
        if (len(tags) > 0):
            compressed_bytes = map_compressor.compress(tags)
            nodes_file.write(struct.pack("!H",len(compressed_bytes)))
            nodes_file.write(compressed_bytes)
        else:
            nodes_file.write(b"\x00\x00")
    elif (current_class == osmium.osm.Way):
        # ID
        # print(obj.id)
        pass

    elif (current_class == osmium.osm.Relation):
        pass

# Cleanup
end_time = time.time()
print(f"[OK] Done! ({str(round(end_time - start_time))}s)")