import numpy as np


def apply_rle_encoding(data):
    encoded = []
    previous = data[0]
    count = 1
    for current in data[1:]:
        if current == previous:
            count += 1
        else:
            encoded.append((previous, count))
            previous = current
            count = 1
    encoded.append((previous, count))
    return encoded

def apply_rle_decoding(encoded_data):
    decoded = []
    for value, count in encoded_data:
        decoded.extend([value] * count)
    return np.array(decoded, dtype=np.int16)