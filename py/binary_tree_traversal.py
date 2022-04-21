from queue import Queue
# Tree shape
# ----------
#     a
#    / \
#   b   c
#  / \   \
# d   e   f
#
# Implement breadth-first-search and depth-first-search variations

traversal = []  # node values added here in order of traversal


class Node:
    def __init__(self, value, left_child=None, right_child=None):
        self.value = value
        self.left = left_child
        self.right = right_child

    def dfs_preorder_recursive(self):
        traversal.append(self.value)
        if self.left:
            self.left.dfs_preorder_recursive()
        if self.right:
            self.right.dfs_preorder_recursive()

    def dfs_inorder_recursive(self):
        if self.left:
            self.left.dfs_inorder_recursive()
        traversal.append(self.value)
        if self.right:
            self.right.dfs_inorder_recursive()

    def dfs_postorder_recursive(self):
        if self.left:
            self.left.dfs_postorder_recursive()
        if self.right:
            self.right.dfs_postorder_recursive()
        traversal.append(self.value)

    def dfs_preorder_iterative(self):
        stack = []
        stack.append(self)
        while stack:
            node = stack.pop()
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
            traversal.append(node.value)

    def dfs_inorder_iterative(self):
        stack = []
        visited = set()
        stack.append(self)
        while stack:
            node = stack.pop()
            if node in visited:
                traversal.append(node.value)
                continue
            if node.right:
                stack.append(node.right)
            stack.append(node)
            if node.left:
                stack.append(node.left)
            visited.add(node)

    def dfs_postorder_iterative(self):
        stack = []
        visited = set()
        stack.append(self)
        while stack:
            node = stack.pop()
            if node in visited:
                traversal.append(node.value)
                continue
            stack.append(node)
            visited.add(node)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    def bfs(self):
        queue = Queue()
        queue.put(self)
        while not queue.empty():
            node = queue.get()
            traversal.append(node.value)
            if node.left:
                queue.put(node.left)
            if node.right:
                queue.put(node.right)

    def bfs_with_levels(self):
        queue = Queue()
        queue.put((self, 0))
        level = 0
        collection = []
        while not queue.empty():
            node, node_level = queue.get()
            if node.left:
                queue.put((node.left, node_level + 1))
            if node.right:
                queue.put((node.right, node_level + 1))

            if level != node_level:
                traversal.append(collection)
                collection = []
                level = node_level
            collection.append(node.value)
        traversal.append(collection)

    def maximum_depth(self):
        queue = Queue()
        queue.put((self, 1))
        while not queue.empty():
            node, node_level = queue.get()
            if node.left:
                queue.put((node.left, node_level + 1))
            if node.right:
                queue.put((node.right, node_level + 1))
        return node_level

    def is_symmetrical_recursive(self):
        left_subtree = []
        right_subtree = []

        self._left_traversal_helper(left_subtree)
        self._right_traversal_helper(right_subtree)

        return left_subtree == right_subtree

    def _left_traversal_helper(self, collection):
        if self.left:
            self.left._left_traversal_helper(collection)
        collection.append(self.value)
        if self.right:
            self.right._left_traversal_helper(collection)

    def _right_traversal_helper(self, collection):
        if self.right:
            self.right._right_traversal_helper(collection)
        collection.append(self.value)
        if self.left:
            self.left._right_traversal_helper(collection)


root = Node('a', Node('b', Node('d'), Node('e')), Node('c', None, Node('f')))

if __name__ == "__main__":

    root.dfs_preorder_recursive()
    assert traversal == ['a', 'b', 'd', 'e', 'c', 'f']
    traversal.clear()

    root.dfs_inorder_recursive()
    assert traversal == ['d', 'b', 'e', 'a', 'c', 'f']
    traversal.clear()

    root.dfs_postorder_recursive()
    assert traversal == ['d', 'e', 'b', 'f', 'c', 'a']
    traversal.clear()

    root.dfs_preorder_iterative()
    assert traversal == ['a', 'b', 'd', 'e', 'c', 'f']
    traversal.clear()

    root.dfs_inorder_iterative()
    assert traversal == ['d', 'b', 'e', 'a', 'c', 'f']
    traversal.clear()

    root.dfs_postorder_iterative()
    assert traversal == ['d', 'e', 'b', 'f', 'c', 'a']
    traversal.clear()

    root.bfs()
    assert traversal == ['a', 'b', 'c', 'd', 'e', 'f']
    traversal.clear()

    root.bfs_with_levels()
    assert traversal == [['a'], ['b', 'c'], ['d', 'e', 'f']]
    traversal.clear()

    assert root.maximum_depth() == 3

    # check that tree is symmetrical
    #      1
    #    /  \
    #   2    2
    #  / \  / \
    # 3   4 4  3

    symmetrical_tree = Node('1',
                            Node('2', Node('3'), Node('4')),
                            Node('2', Node('4'), Node('3')))

    assert symmetrical_tree.is_symmetrical_recursive()

    # check that tree is not symmetrical
    #      1
    #    /  \
    #   2    2
    #    \    \
    #     3    3

    non_symmetrical_tree = Node('1',
                                Node('2', None, Node('3')),
                                Node('2', None, Node('3')))

    assert not non_symmetrical_tree.is_symmetrical_recursive()
