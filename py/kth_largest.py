class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def print_inorder(self):
        """Visualize the tree in order"""
        if self.left:
            self.left.print_inorder()
        print(self.value, end="")
        if self.right:
            self.right.print_inorder()


class KthLargest:
    def __init__(self, k, initial_nums):
        self.k = k
        self.root = None
        self._build_bst(initial_nums)

    def add(self, number):
        self.root = self._insert(self.root, number)
        return self.get_kth_largest()

    def get_kth_largest(self):
        # count backwards in order k-1 times
        
        k, kth_largest = self._inorder_backwards(self.root, self.k)
        return kth_largest

    def _inorder_backwards(self, node, k):
        
        if node.right:
            k, kth_largest = self._inorder_backwards(node.right, k)
        
        if k == 0:
            # we already found the kth_largest
            return k, kth_largest

        k -= 1
        kth_largest = node.value
        
        if k == 0:
            # Current node is kth_largest
            return k, kth_largest
            
        if node.left:
            k, kth_largest = self._inorder_backwards(node.left, k)
        return k, kth_largest
      
    def _build_bst(self, nums):
        for num in nums:
            self.root = self._insert(self.root, num)

    def _insert(self, node, number):
        if node is None:
            node = TreeNode(number)
        elif number < node.value:
            node.left = self._insert(node.left, number)
        else:
            node.right = self._insert(node.right, number)
        return node


nums = [4, 5, 8, 2]
kth_largest = KthLargest(3, nums)

# tests
assert kth_largest.add(3) == 4
assert kth_largest.add(5) == 5
assert kth_largest.add(10) == 5
assert kth_largest.add(9) == 8
assert kth_largest.add(4) == 8


nums = []
kth_largest = KthLargest(1, nums)

assert kth_largest.add(3) == 3
assert kth_largest.add(2) == 3
assert kth_largest.add(5) == 5
