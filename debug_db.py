# Code needs refactoring and is probably not useful anymore.

import os

import modules.map_compressor as map_compressor
from values import config

counter = 0

nodes_file_size = os.path.getsize(f"{config['database']}/nodes.index.bin")
with open(f"{config['database']}/nodes.index.bin","rb") as nodes_file:
    last_id = -1
    while (nodes_file.tell() < nodes_file_size):
        # ID (for index only)
        id = int.from_bytes(nodes_file.read(8),"big")
        nodes_file.seek(9,1)
        # print(id)
        if (id < last_id):
            raise ValueError


        # if (True):
        #     # Lat + Lon
        #     lat = (int.from_bytes(nodes_file.read(4),"big") / (10 ** 7))
        #     lon = (int.from_bytes(nodes_file.read(4),"big") / (10 ** 7))
        #     # Tags
        #     tags_length = int.from_bytes(nodes_file.read(2),"big")
        #     if (tags_length > 0):
        #         tags_dict = map_compressor.decompress(nodes_file.read(tags_length))
        #     else:
        #         tags_dict = {}
        # else:
        #     nodes_file.seek(8,1)
        #     tags_length = int.from_bytes(nodes_file.read(2),"big")
        #     nodes_file.seek(tags_length,1)
        
        counter = counter + 1

print(counter)