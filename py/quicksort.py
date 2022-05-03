#!/usr/bin/env python
"""
Quicksort snippet in python

Was published at: http://blog.pynbo.or.ke/quicksort-python.html
"""
from __future__ import print_function
import random

# We have a list of 10 unsorted integers between 1 and 100 inclusive
list_to_sort = [random.randint(1, 100) for i in range(10)]
print("List before sorting: ", list_to_sort)


"""
As a divide end conquer algorithm, three main steps are involved

 - Pick an element (pivot) in the list

 - Partition the list so that all elements smaller than the pivot
   come before it and those bigger than the pivot come after it

 - Recursively apply the previous steps to the smaller sublists
   before and after the pivot

This should leave you with a sorted list in the end
"""

# Define the quicksort function
def quicksort(L, lo, hi):
    """Sorts elements between indices lo and hi inclusive
    
    L - a list to sort
    lo - index of the lower to begin from
    hi - index of the higher end"""

    # Base case: lo and hi are equal, i.e. only one element in sublist
    # In this case, nothing is done on the list

    if lo < hi:
        # lo is less than hi, i.e. at least two elements in sublist

        # the partitioning step, p is the final position of the
        # pivot after partitioning
        p = partition(L, lo, hi)
        print("Position of pivot..", p)

        # Recursively sort the 'less than partition
        print("Less than %d partition %r " % (L[p], L[lo:p]))
        quicksort(L, lo, p - 1)

        # Recursively sort the 'greater than partition
        print("Greater than %d partition %r " % (L[p], L[p+1:hi+1]))
        quicksort(L, p + 1, hi)

        # and that's it :-)
        # no wait, we have to look at how partitioning is done


def partition(L, lo, hi):
    """Partitions the list within the given range

    L - a list to partition
    lo - index of the lower end in list to start partitioning from
    hi - index of higher end in list to end the partitioning"""

    # There several schemes used to pick the pivot
    # Here we shall use a one known as the 'Lomuto partition scheme'
    # Where we simply pick the last item in the range as the pivot

    pivot = L[hi]

    # i is the next position in the list where we
    # place an element less than or equal to the pivot

    # We begin at the lower end
    i = lo

    # We iterate through the list from lo to hi - 1 (the pivot is at hi, remember?)
    # separating elements less than or equal to the pivot
    # from those greater than the pivot
    j = lo
    while j < hi:
        # if element at j is less than or equal to the pivot
        # swap it into location i
        if L[j] <= pivot:
            L[i], L[j] = L[j], L[i]
            i += 1 # and increment i

        # increment j
        j += 1

    # When the loop completes, we know that all elements before i are less than
    # or equal to the pivot, and all elements from i onwards are greater than
    # the pivot

    # swap the pivot into it's correct position, separating these two parts
    L[i], L[hi] = L[hi], L[i]

    # Now the pivot is at position i, and all elements after i are greater than
    # it

    # return it's position
    return i


# Now let's sort the list
last_index = len(list_to_sort) - 1
quicksort(list_to_sort, 0, last_index)

print("List after sorting: ", list_to_sort)
