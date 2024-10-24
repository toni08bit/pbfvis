## regions.bin

# y0 (invisible and only saved in index file)
## x0 (")
### z0 (this is saved in the bin file and NOT in the index file)
#### very large nodes
### z[1-14]
#### z15
##### very small nodes, only visible when zoomed in at zoom level 15
## x1
## x2
# y1
## x0
## x1
## x2

## regions.index.bin
# same functionality as other index files (actual y,x (except z) are not stored in regions.bin file)

import os
import math
import time

import modules.calc_2d as calc_2d
from values import config

db_files = { # "None" will be replaced by the file append and overwrite handlers
    "regions.bin": None,
    "regions.index.bin": None,
    "regions.counter.bin": None
}

y_factor = int(1 / config["y_chunk_size"])
x_factor = int(1 / config["x_chunk_size"])

def file_size(file_handle):
    start_pos = file_handle.tell()
    file_handle.seek(0,2)
    file_size = file_handle.tell()
    file_handle.seek(start_pos,0)
    return file_size

def get_counter_position(x,y):
    chunk_index = ((y + (90 * y_factor)) * (360 * x_factor) + (x + (180 * x_factor)))

    return (4 + (chunk_index * 7) + 4)


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

# Intialization
print("[INFO] Preparing counter file.")
start_time = time.time()
db_files["regions.counter.bin"][0].write(y_factor.to_bytes(2,"big") + x_factor.to_bytes(2,"big"))
for y_chunk in range((-90 * y_factor),(90 * y_factor),1):
    # y_chunk = (y_chunk / y_factor)
    for x_chunk in range((-180 * x_factor),(180 * x_factor),1):
        # x_chunk = (x_chunk / x_factor)
        db_files["regions.counter.bin"][0].write(y_chunk.to_bytes(2,"big",signed = True) + x_chunk.to_bytes(2,"big",signed = True))
        db_files["regions.counter.bin"][0].write((0).to_bytes(3,"big"))

# Iteration
print("[INFO] Starting.")
with (
    open(f"{config['database']}/nodes.index.bin","rb") as nodes_index_file,
    open(f"{config['database']}/nodes.bin","rb") as nodes_file,
    open(f"{config['database']}/ways.index.bin","rb") as ways_index_file,
    open(f"{config['database']}/ways.bin","rb") as ways_file,
    open(f"{config['database']}/relations.index.bin","rb") as relations_index_file,
    open(f"{config['database']}/relations.bin","rb") as relations_file
):
    nodes_index_length = file_size(nodes_index_file)
    nodes_length = file_size(nodes_file)
    ways_index_length = file_size(ways_index_file)
    ways_length = file_size(ways_file)
    relations_index_length = file_size(relations_index_file)
    relations_length = file_size(relations_file)

    nodes_index_file.seek(0,0)
    chunk_max = 0
    while (nodes_index_file.tell() < nodes_index_length):
        node_id = int.from_bytes(nodes_index_file.read(8),"big")
        node_ref = int.from_bytes(nodes_index_file.read(9),"big")

        nodes_file.seek(node_ref,0)
        node_lat = (int.from_bytes(nodes_file.read(4),"big") / (10 ** 7))
        node_lon = (int.from_bytes(nodes_file.read(4),"big") / (10 ** 7))
        nodes_file.seek(int.from_bytes(nodes_file.read(2),"big"),1)

        y_chunk = math.floor(node_lat / config["y_chunk_size"])
        x_chunk = math.floor(node_lon / config["x_chunk_size"])

        counter_pos = get_counter_position(x_chunk,y_chunk)
        db_files["regions.counter.bin"][1].seek(counter_pos,0)
        current_number = int.from_bytes(db_files["regions.counter.bin"][1].read(3),"big")
        db_files["regions.counter.bin"][1].seek(-3,1)
        chunk_max = max(chunk_max,(current_number + 1))
        db_files["regions.counter.bin"][1].write((current_number + 1).to_bytes(3,"big"))



# Cleanup
for db_file_list in db_files.values():
    for current_file in db_file_list:
        if (not current_file.closed):
            current_file.close()
print("[OK] Done!")
print(chunk_max)