import math

key_size = 8
value_size = 9

def _read_key(file_handler,index):
    file_handler.seek((index * (key_size + value_size)),0)
    key_bytes = file_handler.read(key_size)
    return int.from_bytes(key_bytes,"big")

def _read_record(file_handler,index):
    file_handler.seek((index * (key_size + value_size)),0)
    return file_handler.read(key_size + value_size)

def _write_record(file_handler,index,record):
    file_handler.seek((index * (key_size + value_size)),0)
    file_handler.write(record)

def _heapify(file_handler,n,i):
    largest = i
    left = (2 * i + 1)
    right = (2 * i + 2)

    if (left < n) and (_read_key(file_handler,left) > _read_key(file_handler,largest)):
        largest = left

    if (right < n) and (_read_key(file_handler,right) > _read_key(file_handler,largest)):
        largest = right

    if (largest != i):
        record_i = _read_record(file_handler,i)
        record_largest = _read_record(file_handler,largest)

        _write_record(file_handler,i,record_largest)
        _write_record(file_handler,largest,record_i)

        _heapify(file_handler,n,largest)

def _print_progress(total,counter,last_progress):
    current_progress = (counter / total)
    if ((last_progress != None) and ((current_progress - last_progress) < 0.05)):
        return last_progress
    print(f"[INFO - HEAP SORT] Progress: {str(math.floor(current_progress * 100))}%.")
    return current_progress

def heap_sort(file_handler):
    file_handler.seek(0,2)
    file_size = file_handler.tell()
    n = round(file_size / (key_size + value_size))

    range_a = range((n // 2 - 1),-1,-1)
    range_b = range((n - 1),0,-1)
    i_counter = 0
    last_progress = None
    print("[INFO - HEAP SORT] Starting first heapify.")
    for i in range_a:
        last_progress = _print_progress((len(range_a) + len(range_b)),i_counter,last_progress)
        i_counter = (i_counter + 1)

        _heapify(file_handler,n,i)

    print("[INFO - HEAP SORT] Starting swap loop.")
    for i in range_b:
        last_progress = _print_progress((len(range_a) + len(range_b)),i_counter,last_progress)
        i_counter = (i_counter + 1)

        record_0 = _read_record(file_handler,0)
        record_i = _read_record(file_handler,i)

        _write_record(file_handler,0,record_i)
        _write_record(file_handler,i,record_0)

        _heapify(file_handler,i,0)

    print(f"[OK - HEAP SORT] Sorted (counter: {str(i_counter)}).")