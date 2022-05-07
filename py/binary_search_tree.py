"""Binary Search Tree Operations"""


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def find(node, target_value):
    """Returns a subtree rooted with the given value"""
    if node is None:
        return None
    if node.value == target_value:
        return node
    if target_value < node.value:
        return find(node.left, target_value)
    if target_value > node.value:
        return find(node.right, target_value)


def find_iterative(node, target_value):

    current_node = node
    while current_node is not None:
        if current_node.value == target_value:
            return current_node
        if target_value < current_node.value:
            current_node = current_node.left
        elif target_value > current_node.value:
            current_node = current_node.right
    return None  # implicit in python tho


def insert(node, value):
    if value < node.value:
        if node.left is None:
            node.left = TreeNode(value)
        else:
            insert(node.left, value)
    else:
        if node.right is None:
            node.right = TreeNode(value)
        else:
            insert(node.right, value)


#def delete(node, target):
#    pass


if __name__ == "__main__":
    # Search binary tree:
    #     4
    #    / \
    #   2   6
    #  / \
    # 1   3
    root = TreeNode(4,
                    TreeNode(2,
                             TreeNode(1),
                             TreeNode(3)),
                    TreeNode(6))

    subtree = find(root, 2)
    assert subtree.value == 2
    assert subtree.left.value == 1
    assert subtree.right.value == 3

    subtree = find(root, 5)
    assert subtree is None

    subtree = find_iterative(root, 2)
    assert subtree.value == 2
    assert subtree.left.value == 1
    assert subtree.right.value == 3

    subtree = find_iterative(root, 5)
    assert subtree is None

    # Insert into binary search tree
    #     4
    #    / \
    #   2   6
    #  / \
    # 1   3

    insert(root, 5)
    assert root.right.left.value == 5

    # Delete from binary search tree
    #      5
    #    /   \
    #   3     7
    #  / \   / \
    # 2   4 6   8
    
#   new_root = delete(root, 5)
#   assert new_root.value == 6
#   assert new_root.right.left is None
#   assert new_root.right.right == 8
