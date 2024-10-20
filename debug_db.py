import os
import struct

import modules.map_compressor as map_compressor
from values import config

nodes_file_size = os.path.getsize(f"{config['database']}/nodes.bin")
with open(f"{config['database']}/nodes.bin","rb") as nodes_file:
    while (nodes_file.tell() < nodes_file_size):
        # ID
        node_id = struct.unpack("!Q",nodes_file.read(8))[0]
        # Lat + Lon
        lat = (struct.unpack("!i",nodes_file.read(4))[0] / (10 ** 7))
        lon = (struct.unpack("!i",nodes_file.read(4))[0] / (10 ** 7))
        # Tags
        tags_length = struct.unpack("!H",nodes_file.read(2))[0]
        if (tags_length > 0):
            tags_dict = map_compressor.decompress(nodes_file.read(tags_length))
        else:
            tags_dict = {}
        
