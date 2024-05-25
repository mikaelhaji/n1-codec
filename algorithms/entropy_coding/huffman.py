import heapq
import json
from collections import Counter

class HuffmanNode:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(symbol_frequencies):
    heap = [(freq, HuffmanNode(symbol, freq)) for symbol, freq in symbol_frequencies.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged_node = HuffmanNode(left=left[1], right=right[1], frequency=left[0] + right[0])
        heapq.heappush(heap, (merged_node.frequency, merged_node))
    return heap[0][1]

def generate_huffman_codes(node, path=""):
    if node is None:
        return {}
    if node.is_leaf():
        return {node.symbol: path}
    codes = {}
    codes.update(generate_huffman_codes(node.left, path + "0"))
    codes.update(generate_huffman_codes(node.right, path + "1"))
    return codes

def create_canonical_huffman_code(symbol_codes):
    sorted_symbols = sorted(symbol_codes.items(), key=lambda item: (len(item[1]), item[0]))
    length = 0
    code = 0
    canonical_codes = {}
    for symbol, old_code in sorted_symbols:
        if length != len(old_code):
            code <<= (len(old_code) - length)
            length = len(old_code)
        canonical_codes[symbol] = f"{code:0{length}b}"
        code += 1
    return canonical_codes

def compress_data_canonical(data, canonical_codes):
    encoded_data = ''.join(canonical_codes[symbol] for symbol in data)
    padding = (8 - len(encoded_data) % 8) % 8
    encoded_data += '0' * padding
    encoded_bytes = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, 'big')
    return encoded_bytes, padding

def serialize_huffman_tree(canonical_codes):
    return json.dumps({int(symbol): code for symbol, code in canonical_codes.items()})

def compress_huffman(data):
    symbol_freqs = Counter(data)
    huffman_tree = build_huffman_tree(symbol_freqs)
    symbol_codes = generate_huffman_codes(huffman_tree)
    canonical_codes = create_canonical_huffman_code(symbol_codes)
    encoded_bytes, padding = compress_data_canonical(data, canonical_codes)
    serialized_tree = serialize_huffman_tree(canonical_codes)
    return encoded_bytes, serialized_tree, padding

def deserialize_huffman_tree(codes):
    root = HuffmanNode()
    for symbol, code in sorted(codes.items(), key=lambda item: (len(item[1]), item[1])):
        current_node = root
        for bit in code:
            if bit == '0':
                if not current_node.left:
                    current_node.left = HuffmanNode()
                current_node = current_node.left
            else:
                if not current_node.right:
                    current_node.right = HuffmanNode()
                current_node = current_node.right
        current_node.symbol = symbol
    return root

def decompress_huffman(encoded_bytes, root, original_length):
    binary_string = ''.join(f'{byte:08b}' for byte in encoded_bytes)
    decoded_symbols = []
    current_node = root
    for bit in binary_string:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.is_leaf():
            decoded_symbols.append(current_node.symbol)
            current_node = root
    return decoded_symbols[:original_length]