import struct
import zlib

def compress(given_dict):
    map_bytes = b""
    for key,value in given_dict.items():
        if ((type(key) != str) or (type(value) != str)):
            raise TypeError("The key/value must be a string.")
        key = key.encode("utf-8")
        value = value.encode("utf-8")
        key_length = len(key)
        value_length = len(value)
        if (key_length >= (2 ** (1 * 8))):
            raise ValueError("The size of the key's length may not be bigger than 2 bytes.")
        if (value_length >= (2 ** (4 * 8))):
            raise ValueError("The size of the value's length may not be bigger than 4 bytes.")
        
        # Key + Value Length
        map_bytes = (map_bytes + struct.pack("!B",key_length) + struct.pack("!I",value_length))
        map_bytes = (map_bytes + key + value)
    
    zlib_bytes = zlib.compress(map_bytes)
    if (len(zlib_bytes) < len(map_bytes)):
        return (b"\x01" + zlib_bytes)
    else:
        return (b"\x00" + map_bytes)

def decompress(given_bytes):
    map_bytes = given_bytes[1:]
    if (given_bytes[:1] == b"\x01"):
        map_bytes = zlib.decompress(map_bytes)
    
    map_dict = {}
    while (len(map_bytes) > 0):
        key_length = struct.unpack("!B",map_bytes[:1])[0]
        value_length = struct.unpack("!I",map_bytes[1:5])[0]
        key = map_bytes[5:(5 + key_length)]
        value = map_bytes[(5 + key_length):(5 + key_length + value_length)]
        map_dict[key.decode("utf-8")] = value.decode("utf-8")
        map_bytes = map_bytes[(5 + key_length + value_length):]

    return map_dict