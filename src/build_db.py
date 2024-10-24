import os
import time
import osmium
import osmium.osm

import modules.map_compressor as map_compressor
import modules.order_operations as order_operations
from values import config

db_files = { # "None" will be replaced by the file append and overwrite handlers
    "nodes.bin": None,
    "nodes.index.bin": None,
    "ways.bin": None,
    "ways.index.bin": None,
    "relations.bin": None,
    "relations.index.bin": None
}

# Check
if (__name__ != "__main__"):
    raise RuntimeError("This is not a module.")
for current_file in db_files.keys():
    if (os.path.exists(f"{config['database']}/{current_file}")):
        raise FileExistsError(f"{current_file} already exists.")
    else:
        db_files[current_file] = [
            open(f"{config['database']}/{current_file}","ab"),
            open(f"{config['database']}/{current_file}","r+b")
        ]

# Functions
def pack_tags(file_handler,tags):
    if (len(tags) > 0):
        compressed_bytes = map_compressor.compress(tags)
        file_handler.write(len(compressed_bytes).to_bytes(2,"big"))
        file_handler.write(compressed_bytes)
    else:
        file_handler.write((0).to_bytes(2,"big"))

def close_db_file(db_file_name):
    for file_handler in db_files[db_file_name]:
        if (not file_handler.closed):
            file_handler.close()

# Initialization
print("[INFO] Opening file.")
file_processor = osmium.FileProcessor(config['pbf_input'])
print("[INFO] Starting.")
start_time = time.time()
last_class = None

# Iteration
object_count = 0
for obj in file_processor:
    current_class = obj.__class__
    if (last_class != current_class):
        if (last_class == osmium.osm.Node):
            order_operations.heap_sort(db_files["nodes.index.bin"][1])
            close_db_file("nodes.bin")
            close_db_file("nodes.index.bin")
        elif (last_class == osmium.osm.Way):
            order_operations.heap_sort(db_files["ways.index.bin"][1])
            close_db_file("ways.bin")
            close_db_file("ways.index.bin")
        print(f"[INFO] Processing class: {current_class.__name__}.")
        last_class = current_class

    tags = dict(obj.tags)    
    object_count = (object_count + 1)
    if (current_class == osmium.osm.Node):
        # ID
        db_files["nodes.index.bin"][0].write(obj.id.to_bytes(8,"big"))
        db_files["nodes.index.bin"][0].write(db_files["nodes.bin"][0].tell().to_bytes(9,"big"))
        # Lat + Lon
        db_files["nodes.bin"][0].write(round(obj.lat * (10 ** 7)).to_bytes(4,"big",signed = True) + round(obj.lon * (10 ** 7)).to_bytes(4,"big",signed = True))
        # Tags
        pack_tags(db_files["nodes.bin"][0],tags)
    elif (current_class == osmium.osm.Way):
        # ID
        db_files["ways.index.bin"][0].write(obj.id.to_bytes(8,"big"))
        db_files["ways.index.bin"][0].write(db_files["ways.bin"][0].tell().to_bytes(9,"big"))
        # Area Check
        way_nodes = list(obj.nodes)
        if (way_nodes[0].ref == way_nodes[-1].ref):
            db_files["ways.bin"][0].write(b"\x01")
            del way_nodes[-1]
        else:
            db_files["ways.bin"][0].write(b"\x00")
        # Nodes
        db_files["ways.bin"][0].write(len(way_nodes).to_bytes(2,"big"))
        for current_node in way_nodes:
            db_files["ways.bin"][0].write(current_node.ref.to_bytes(8,"big"))
        # Tags
        pack_tags(db_files["ways.bin"][0],tags)
    elif (current_class == osmium.osm.Relation):
        # ID
        db_files["relations.index.bin"][0].write(obj.id.to_bytes(8,"big"))
        db_files["relations.index.bin"][0].write(db_files["relations.bin"][0].tell().to_bytes(9,"big"))
        # Members
        members = list(obj.members)
        db_files["relations.bin"][0].write(len(members).to_bytes(2,"big"))
        for member in members:
            db_files["relations.bin"][0].write(map_compressor.get_object_type_id(member.type))
            db_files["relations.bin"][0].write(len(member.role).to_bytes(1,"big"))
            db_files["relations.bin"][0].write(member.role.encode("utf-8"))
            db_files["relations.bin"][0].write(member.ref.to_bytes(8,"big"))
        # Tags
        pack_tags(db_files["relations.bin"][0],tags)

    if ((object_count % (10 ** 5)) == 0):
        print(f"[INFO] Progress: {str(round(object_count / (10 ** 5)))}*10^5 objects.")

order_operations.heap_sort(db_files["relations.index.bin"][1])
close_db_file("relations.bin")
close_db_file("relations.index.bin")


# Cleanup
end_time = time.time()
for db_file_list in db_files.values():
    for current_file in db_file_list:
        if (not current_file.closed):
            current_file.close()
print(f"[OK] Done! ({str(round(end_time - start_time))}s)")
