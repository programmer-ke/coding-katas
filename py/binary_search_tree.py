"""Binary Search Tree Operations"""


class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"""
        TreeNode({self.value},
          {self.left},
          {self.right})
        """


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
    """Returns a subtree rooted with the given value"""
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


def delete(root, target):
    """Delete node referencing target from tree """

    target_subtree, parent = _find_delete_target(root, target)

    if target_subtree is None:
        # Delete target not found, nothing to do..
        return root

    replacement_value = None
    if target_subtree.right:
        replacement_value = _retrieve_smallest_value(target_subtree.right, parent=target_subtree)
    elif target_subtree.left:
        replacement_value = _retrieve_largest_value(target_subtree.left, parent=target_subtree)

    if replacement_value is not None:
        target_subtree.value = replacement_value

    # from this point on, target is a leaf node
    # simply unhook from parent if it has one
    elif parent is None:
        # deleting root node with no children
        # return None as the root
        return None
    elif parent.value < target_subtree.value:
        parent.right = None
    else:
        parent.left = None
    return root

def _retrieve_smallest_value(current_node, parent):
    """Given subtree, return its smallest value having deleted its node"""
    
    if current_node.left:
        return _retrieve_smallest_value(current_node.left, current_node)

    # From this point, current node has the smallest value
    # replace current node in tree
    if current_node.value < parent.value:
        # current node is parent's left child
        parent.left = current_node.right
    else:
        # current node is parent's right child
        parent.right = current_node.right
    return current_node.value

def _retrieve_largest_value(current_node, parent):
    """Given a subtree, return its largest value having deleted it's node"""
    
    if current_node.right:
        return _retrieve_largest_value(current_node.right, current_node)


    # From this point, current node has the largest value in subtree
    # replace current node in tree
    if current_node.value < parent.value:
        # current node is parent's left child
        parent.left = current_node.left
    else:
        # current node is parent's right child
        parent.right = current_node.left
    return current_node.value


def _find_delete_target(root, target):
    """Returns the subtree with matching target and its parent node"""

    current_node = root
    parent = None

    while (current_node is not None and current_node.value != target) :

        parent = current_node
        if current_node.value < target:
            current_node = current_node.right
        else:
            current_node = current_node.left
        
    return current_node, parent

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

    root = TreeNode(5,
                    TreeNode(3,
                             TreeNode(2),
                             TreeNode(4)),
                    TreeNode(7,
                             TreeNode(6),
                             TreeNode(8)))

    new_root = delete(root, 5)
    assert new_root.value == 6
    assert new_root.right.left is None
    assert new_root.right.right.value == 8

    # Tree now looks like below
    #      6
    #    /   \
    #   3     7
    #  / \     \
    # 2   4     8
    # 
    # Delete 7, 8 should take its place

    new_root = delete(new_root, 7)
    assert new_root.right.value == 8

    # Tree now looks like below
    #      6
    #    /   \
    #   3     8
    #  / \     
    # 2   4     
    # 
    # Delete 6, 8 should take its place

    new_root = delete(new_root, 6)
    assert new_root.value == 8
    assert new_root.right is None

    # Tree now looks like below
    #     8
    #    /   
    #   3     
    #  / \     
    # 2   4     
    # 
    # Delete 8, 4 should take its place
    new_root = delete(new_root, 8)
    assert new_root.value == 4
    assert new_root.right is None
    assert new_root.left.value == 3

    root = TreeNode(4)
    new_root = delete(root, 4)
    assert new_root is None
