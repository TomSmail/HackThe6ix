# Drone Code - quentin
try:
    import struct
except ImportError:
    import ustruct as struct

def encode_double(value: float) -> bytes:
    return struct.pack('<d', value)


def locationResponse(lat: float, long: float) -> bytes:
    bts = [9] + [b for b in encode_double(lat)] + [17] + [b for b in encode_double(long)]
    return bytes(bts)


def insecticideResponse(successful: bool, outofjuice: bool) -> bytes:
    if successful is False and outofjuice is True:
        return bytes([16, 1])
    if successful is True and outofjuice is True:
        return bytes([8, 1, 16, 1])
    if successful is True and outofjuice is False:
        return bytes([8, 1])


def whichRequestType(protomessage: bytes) -> int:
    if protomessage == b'\x08\x01':
        return 1  # Location
    elif protomessage == b'\x08\x02':
        return 2  # insecticide
    else:
        raise Exception
