import sys
from collections import defaultdict


def naive_hash(data):
    sum(data) % 13

def find_groups(filenames):
    groups = defaultdict(set)
    for filename in filenames:
        content = open(filename, "rb").read()
        hash_code = naive_hash(content)
        groups[hash_code].add(filename)
    return groups


def find_duplicates(filenames):
    matches = []
    for i_left in range(len(filenames)):
        left = filenames[i_left]
        for i_right in range(i_left):
            right = filenames[i_right]
            if same_bytes(left, right):
                matches.append((left, right))
    return matches



def same_bytes(left_name, right_name):
    left_bytes = open(left_name, "rb").read()
    right_bytes = open(right_name, "rb").read()
    return left_bytes == right_bytes


if __name__ == "__main__":
    groups = find_groups(sys.argv[1:])
    for filenames in groups.values():
        duplicates = find_duplicates(list(filenames))
        for left, right in duplicates:
            print(left, right)
