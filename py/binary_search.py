"""Simple binary search"""


def find(list_, target):

    def binary_search(list_, target, min_index, max_index):
        if max_index < min_index:
            return None
        mid_index = (min_index + max_index) // 2
        mid_value = list_[mid_index]
        if mid_value == target:
            return mid_value
        if mid_value < target:
            return binary_search(list_, target, mid_index + 1, max_index)
        else:
            return binary_search(list_, target, min_index, mid_index - 1)

    return binary_search(list_, target, 0, len(list_) - 1)


if __name__ == "__main__":
    numbers = [1, 2, 4, 7, 9, 11, 15, 30, 33, 37]

    assert find([], 3) is None
    assert find(numbers, 9) == 9
    assert find(numbers, 2) == 2
    assert find(numbers, 33) == 33
    assert find(numbers, 50) is None
    assert find(numbers, 0) is None
