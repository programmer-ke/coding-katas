"""Reverse a linked list"""


class LinkedList:
    """Represents a singly-linked list"""

    def __init__(self, list_):
        """Build a linked list from the provided list

        Sets an attribute `head` with points to the first node of the
        linked list"""

        self._head = None
        current = None
        for i in list_:
            if self._head is None:
                self._head = self.Node(i)
                current = self._head
            else:
                current.next = self.Node(i)
                current = current.next

    def _items(self):
        """Generates the linked list values in order"""
        node = self._head
        while node:
            yield node.value
            node = node.next

    def reverse(self):
        current = self._head
        prev = None
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        self._head = prev

    def __iter__(self):
        return self._items()

    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None


if __name__ == "__main__":
    ll = LinkedList([])
    assert list(ll) == []
    ll.reverse()
    assert list(ll) == []

    ll = LinkedList([1])
    assert list(ll) == [1]
    ll.reverse()
    assert list(ll) == [1]

    ll = LinkedList([1, 2, 'a'])
    assert list(ll) == [1, 2, 'a']
    ll.reverse()
    assert list(ll) == ['a', 2, 1]
