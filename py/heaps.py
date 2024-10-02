"""
A binary heap implementation.

There are two types of heaps, a max heap where any node value cannot
be less than any of its childrens', and a min heap, where any node
value cannot be greater than any of its childrens'.

Operations:

- heapify: create a heap out of a list used to initialize the heap
- push: Add an item to the heap
- top: Return the topmost item in the heap, the maximum in a max heap and
       the minimum in a min heap.
- pop: Remove the topmost item of the heap
"""


class Heap:
    def __init__(self, nodes, comparator):
        self._tree = nodes[:]
        self._comparator = comparator
        self._heapify()

    def top(self):
        """Return topmost item if it exists"""
        if self._tree:
            return self._tree[0]

    def pop(self):
        """Replace topmost item if it exists and return it"""
        if self._tree:
            old_top = self.top()
            last_node = self._tree.pop()
            if self._tree:
                self._tree[0] = last_node
                self._sift_down(0)
            return old_top

    def push(self, item):
        """Add item to heap at its correct position"""
        self._tree.append(item)
        new_item_index = len(self._tree) - 1
        parent_index = self._parent(new_item_index)

        while not parent_index < 0 and self._comparator(
            self._tree[new_item_index], self._tree[parent_index]
        ):
            self._tree[parent_index], self._tree[new_item_index] = (
                self._tree[new_item_index],
                self._tree[parent_index],
            )
            new_item_index = parent_index
            parent_index = self._parent(new_item_index)

    def _heapify(self):
        """Create a heap out of the list of nodes"""

        last_index = len(self._tree) - 1
        for i in range(last_index, -1, -1):
            self._sift_down(i)

    def _sift_down(self, index):
        """Find the correct position of element at index down the tree"""

        minmax = index
        if (left_child_index := self._left_child(index)) < len(self._tree):
            left_child = self._tree[left_child_index]
            if self._comparator(left_child, self._tree[minmax]):
                minmax = left_child_index

        if (right_child_index := self._right_child(index)) < len(self._tree):
            right_child = self._tree[right_child_index]
            if self._comparator(right_child, self._tree[minmax]):
                minmax = right_child_index

        if minmax != index:
            # item at index should switch positions with child
            self._tree[index], self._tree[minmax] = (
                self._tree[minmax],
                self._tree[index],
            )

            # minmax is now the new position, sift down recursively if necessary
            self._sift_down(minmax)

    def _left_child(self, index):
        return index * 2 + 1

    def _right_child(self, index):
        return index * 2 + 2

    def _parent(self, index):
        return (index - 1) // 2


def test():
    # Initialize a heap with a list of values and a comparator
    # function.
    # The function determines whether it is a min or max heap
    nums = [65, 6, 34, 17, 62, 100, 2, 68, 62, 0, 64, 93, 35, 93, 75]

    max_heap = Heap(nums, comparator=lambda x, y: x > y)  # max heap
    assert max_heap.top() == 100

    min_heap = Heap(nums, comparator=lambda x, y: x < y)  # min heap
    assert min_heap.top() == 0

    top = max_heap.pop()
    assert top == 100
    assert max_heap.top() == 93

    top = min_heap.pop()
    assert top == 0
    assert min_heap.top() == 2

    min_heap.push(101)
    assert min_heap.top() == 2

    max_heap.push(101)
    assert max_heap.top() == 101

    # edge cases
    heap = Heap([], lambda x, y: x > y)
    assert heap.top() is None
    assert heap.pop() is None
    heap.push(1)
    assert heap.top() == 1
    assert heap.pop() == 1
    assert heap.pop() is None

if __name__ == "__main__":
    test()
