import asyncio
from struct import*

def bytes_to_hex_str(data):
  return '0x' + ''.join(format(b, '02x') for b in data)


def bytes_to_int(data):
   
    try:
        return int.from_bytes(data, byteorder='big')
    except:
        return data


def int_to_bytes(int_value: int, length: int) -> bytes:
   
    if length == 1:
        fmt = "!B"
    elif length == 2:
        fmt = "!H"
    return pack(fmt, int_value)



def encode_string(string: str) -> bytes:
    data = string.encode(encoding='utf-8')
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data


def encode_data_with_length(data: bytes) -> bytes:
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data


def int_to_bytes_str(value: int) -> bytes:
   return str(value).encode('utf-8')



def read_or_raise(reader, n=-1):
    try:
        data = yield from reader.read(n)
    except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
        data = None
    if not data:
        raise Exception("No more data")
    return data



def decode_string(reader) -> bytes:
    length_bytes = yield from read_or_raise(reader, 2)
    str_length = unpack("!H", length_bytes)
    if str_length[0]:
        byte_str = yield from read_or_raise(reader, str_length[0])
        try:
            return byte_str.decode(encoding='utf-8')
        except:
            return str(byte_str)
    else:
        return ''



def decode_data_with_length(reader) -> bytes:
    length_bytes = yield from read_or_raise(reader, 2)
    bytes_length = unpack("!H", length_bytes)
    data = yield from read_or_raise(reader, bytes_length[0])
    return data


def decode_packet_id(reader) -> int:
    packet_id_bytes = yield from read_or_raise(reader, 2)
    packet_id = unpack("!H", packet_id_bytes)
    return packet_id[0]

