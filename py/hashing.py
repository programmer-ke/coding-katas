"""Hashing in python"""

import hashlib

variable_length_input = "The quick brown fox jumps over the lazy dog"

fixed_length_hash = hash_function(variable_length_input)

print(fixed_length_hash)
# outputs: d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592

print(len(fixed_length_hash))
# outputs: 64

def hash_function(input_text):
    """Returns a fixed length hash of the input"""

    input_bytes = bytes(input_text, encoding="utf-8")
    return hashlib.sha256(input_bytes).hexdigest()

