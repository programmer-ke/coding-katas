"""
Hashing in python

digraph {
   input [label = "Variable-Length Input"];
   output [lable = "Fixed-Length Output"]
   input -> "hash function" -> output
}
"""

import hashlib

variable_length_input = "The fox jumped over the wall"

def hash_function(input_text):
    """Returns a fixed length hash of the input"""

    input_bytes = bytes(input_text, encoding="utf-8")
    return hashlib.sha256(input_bytes).hexdigest()

fixed_length_output = hash_function(input_text)
len(fixed_length_output)
