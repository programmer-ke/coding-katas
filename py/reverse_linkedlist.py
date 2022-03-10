"""Reverse a linked list"""

class LinkedList:

    def __init__(self, list_):
        self.head = None
        current = None
        for i in list_:
            if self.head is None:
                self.head = self.Node(i)
                current = self.head
            else:
                current.next = self.Node(i)
                current = current.next

    def to_list(self):

        list_ = []
        node = self.head
        while node:
            list_.append(node.value)
            node = node.next
        return list_

    def reverse(self):
        current = self.head
        prev = None
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        self.head = prev

    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None


if __name__ == "__main__":
    ll = LinkedList([])
    assert ll.to_list() == []
    ll.reverse()
    assert ll.to_list() == []

    ll = LinkedList([1])
    assert ll.to_list() == [1]
    ll.reverse()
    assert ll.to_list() == [1]

    ll = LinkedList([1, 2, 'a'])
    assert ll.to_list() == [1, 2, 'a']
    ll.reverse()
    assert ll.to_list() == ['a', 2, 1]
