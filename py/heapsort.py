"""A demonstration of using a heap to sort"""

def heapsort(items):
    """Sort a list in place"""
    
    # build a max-heap starting from the end of the list towards the 
    # beginning
    n = len(items)
    for i in range(n-1, -1, -1):
        sift_down(items, n, i)
    
    # The whole list is now a max-heap
    # Repeatedly pop the largest item from the heap to the end of the
    # list, growing the sorted segment towards the beginning of the list
    for i in range(n-1, 0, -1):
        items[i], items[0] = items[0], items[i]
        
        # sift down the new element at root of the heap
        sift_down(items, i, 0)


def sift_down(items, length, start_index):
    """Sift down element at start_index in the list segment of the given length"""

    left_child_index = 2 * start_index + 1
    right_child_index = 2 * start_index + 2
    largest = start_index

    if left_child_index < length and items[largest] < items[left_child_index]:
        largest = left_child_index

    if right_child_index < length and items[largest] < items[right_child_index]:
        largest = right_child_index
    
    # At this point, largest is the index of the largest item between 
    # element being sifted and the children

    if largest != start_index:
        # The element has not found its position in heap, a child is larger
        # swap element with child and sift down further
        items[start_index], items[largest] = items[largest], items[start_index]
        sift_down(items, length, largest)


nums = [3, 8, 9, 2, 4, 5]
heapsort(nums)

assert nums == sorted(nums)

# Consider some edge cases
nums = [3]
heapsort(nums)
assert nums == [3]
nums = []
heapsort(nums)
assert nums == []
