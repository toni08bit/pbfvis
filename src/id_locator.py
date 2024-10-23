import modules.map_compressor as map_compressor
from values import config

package_size = (8 + 9)

def locate_id(index_file,target_id):
    index_file.seek(0,2)
    index_total = (index_file.tell() // package_size)
    index_file.seek(0,0)

    low = 0
    high = (index_total - 1)

    while (low <= high):
        mid = ((low + high) // 2)
        index_file.seek((mid * package_size),0)

        current_id_bytes = index_file.read(8)
        if (not current_id_bytes):
            break
        
        current_id = int.from_bytes(current_id_bytes,"big")

        if (current_id < target_id):
            low = (mid + 1)
        elif (current_id > target_id):
            high = (mid - 1)
        else:
            return int.from_bytes(index_file,"big")
    
    return None
