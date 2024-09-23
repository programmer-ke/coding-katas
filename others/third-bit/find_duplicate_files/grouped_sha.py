import sys
from hashlib import sha256
from collections import defaultdict


def find_groups(filenames):
    groups = defaultdict(set)
    for filename in filenames:
        content = open(filename, "rb").read()
        hash_code = sha256(content).hexdigest()
        groups[hash_code].add(filename)
    return groups


if __name__ == "__main__":
    groups = find_groups(sys.argv[1:])
    for filenames in groups.values():
        print(", ".join(filenames))
