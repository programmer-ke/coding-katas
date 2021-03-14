# Hash table with separate chaining
# https://stephenagrice.medium.com/how-to-implement-a-hash-table-in-python-1eb6c55019fd

class HashTable:

    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None

        def __repr__(self):
            str_ = "(key: {k}, value: {v}, next: {n})"
            return str_.format(k=self.key, v=self.value, n=self.next)

    def __init__(self):
        self._size = 0
        self._capacity = 10
        self._buckets = [None] * self._capacity

    def set(self, key, value):
        bucket_index = self._hash(key)
        self._bucket_insert(bucket_index, key, value)
        self._size += 1

    def size(self):
        """Return current size"""
        return self._size

    def get(self, key):
        bucket_index = self._hash(key)
        value = self._bucket_retrieve(bucket_index, key)
        return value

    def _hash(self, key):
        # Should distribute keys uniformly across bucket for good
        # perfomance characteristics
        sum_ = 0
        for i, c in enumerate(key):
            sum_ += (i + len(key)) * ord(c)

        return sum_ % self._capacity

    def _bucket_retrieve(self, index, key):
        node = self._buckets[index]
        if node is None:
            raise KeyError

        value = self._traverse_list_for_item(node, key)
        return value

    def _traverse_list_for_item(self, head, key):

        current_node = head
        while current_node is not None:
            if current_node.key == key:
                return current_node.value
            current_node = current_node.next
        else:
            raise KeyError

    def _bucket_insert(self, index, key, value):
        # If key exists, update value,
        # otherwise, create key,value pair
        head = self._buckets[index]
        if head is None:
            new_node = self.Node(key, value)
            self._buckets[index] = new_node
        else:
            self._add_or_update(head, key, value)
        return

    def _add_or_update(self, head, key, value):
        # Traverse linked list, to find key
        # If it doesn't exist, add it at the end

        current_node = head

        while current_node is not None:
            if current_node.key == key:
                current_node.value = value
                break
            previous_node = current_node
            current_node = current_node.next
        else:
            previous_node.next = self.Node(key, value)

    def debug(self):
        print(self._buckets)


if __name__ == "__main__":

    ht = HashTable()
    ht.set("a", 1)
    assert ht.size() == 1

    value = ht.get("a")
    assert value == 1

    keys = ["a", "b", "c", "d", "e", "f", "g", "h"]

    for i, k in enumerate(keys):
        ht.set(k, i+1)

    for i, k in enumerate(keys):
        assert ht.get(k) == i+1

    # test re-assignment
    ht.set("some_key", 1)
    ht.set("some_key", 2)
    assert ht.get("some_key") == 2
