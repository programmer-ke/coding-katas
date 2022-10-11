"""
Problem: Given 2 integers greater than zero, find the largest number
that divides the both equally, i.e their greatest common divisor.

Examples:
gcd(16, 12) = 4
gcd(5, 3) = 1
gcd(20, 40) = 20

Approach one
-----------

Given the numbers m and n, find all the factors of m and of n,
identify the common ones and select the largest.  At least one factor
i.e. 1 is guaranteed to be common.

The problem with this approach is that for large values of m and n, it
will take a large number of checks to find all the factors of the
numbers.

Say for a large value of m, we'll check all the numbers 1..sqrt(m) to
find numbers that divide it perfectly. The set of these numbers and
their complements will form the set of all factors of m.

Approach two
------------

Say we're given two numbers, e.g. 20 and 12.  Their difference is
20 - 12 = 8

Since the gcd of 20 and 12 divides both of them equally, then it is
given that their gcd is the same as the gcd of smaller number 12 and
their difference 8.

We get the difference 12 - 8 = 4.

Likewise, the gcd of 12 and 8 is the same as the gcd of 8 and 4.

The difference between 8 and 4, 8 - 4 = 4.

The gcd of the smaller number 4, and their difference 4, is trivially
4.

The gcd didn't change at any step along the way, therefore, the gcd of
the original numbers, 20 and 12 is also 4.

So at each step, we're turning our problem into a smaller problem,
until we have one we can trivially solve.  This known as the Euclidean
algorithm: https://en.wikipedia.org/wiki/Euclidean_algorithm

In code, this algorithm can be implemented as a loop and for each
iteration we work on a progressively smaller problem until we reach
our termination condition, which is, the difference between the
smaller number and the remainder in the previous iteration is zero.

If the given numbers have a large difference between them, say 80 and
6, we'll have to do a correspondingly larger sequence of subtractions
to get their gcd, which is 2. We'll subtract 6 from the sequence of
larger differences a total of 13 times.

We can find a way of making this process more efficient. Since
repeated subtractions is basically division, we use the modulus
operator since we're only interested in checking the gcd of the
smaller number and the remainder after dividing the larger number by
equal parts.

80 % 6 = 2

Now were interested in the gcd of 6 and 2. We do the same operation
with the smaller numbers

6 % 2 = 0.

Since 2 divides 6 equally, then the gcd of 6 and 2, the same as the 
gcd of 80 and 6 is 2.

Using the modulus operator, we've now cut down significantly on the
number of iterations needed to find the solution.

To implement this in code, we similarly use a loop. Our termination
condition is when the remainder of the modulus operation is zero.
At that point, the divisor is the gcd of the original pair of numbers.

In each iteration, we work on a smaller component of the problem, the
gcd of the remainder and the smaller number in the previous iteration.
"""

def gcd(m, n):
    assert m > 0 and n > 0

    r = m % n
    
    while r > 0:
        m, n = n, r
        r = m % n

    return n

assert gcd(2, 2) == 2
assert gcd(20, 6) == 2
assert gcd(80, 6) == 2
assert gcd(6, 80) == 2  # can you see why this works?
assert gcd(7, 103) == 1
assert gcd(322, 112) == 14


"""
This can also be represented recursively, which maps more closely to
the mental model of progressively reducing the bigger problem into
a smaller problem.

We'll redefine gcd recursively to demonstrate this.
"""

def gcd(m, n):
    assert m > 0 and n > 0
    
    r = m % n
    if r == 0:
        return n

    # gcd of m and n is the same
    # as the gcd of n and r
    return gcd(n, r)

assert gcd(2, 2) == 2
assert gcd(20, 6) == 2
assert gcd(80, 6) == 2
assert gcd(6, 80) == 2
assert gcd(7, 103) == 1
assert gcd(322, 112) == 14

"""
The worst case scenario for this final approach is when calculating
the gcd of subsequent terms in a fibonacci sequence, e.g 34 and 21

The sequence remainders in this case will be:
13, 8, 5, 3, 2, 1, 0

Until we get to 1, we're basically generating the previous terms in
the fibonacci sequence.
"""
