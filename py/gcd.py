"""
Problem: Given 2 integers greater than zero, find the largest number that divides 
the both equally, i.e their greatest common divisor.

Examples:
gcd(16, 12) = 4
gcd(5, 3) = 1
gcd(20, 40) = 20

Approach one
-----------

Given the numbers m and n, find all the factors of n and of m, identify
the common ones and select the largest. 
At least one factor i.e. 1 is guaranteed to be common.

The problem with this approach is that  for large values of m and n,
it will take a large number of checks to find all the factors of the
number.

Say for a large value m, we'll check all the numbers 1..sqrt(m) to find
numbers that divide it perfectly. The set of these numbers and their
complements will form the set of all factors of m.

Approach two
------------

Say we're given two numbers, e.g. 20 and 12.
Their difference is 20 - 12 = 8

Since the gcd of 20 and 12 divides both of them equally, then it is
given that their gcd is the same as the gcd of smaller number 12 and 
their difference 8.

We get the difference 12 - 8 = 4.

Likewise, the gcd of 12 and 8 is the same as the gcd of 8 and 4.

The difference between 8 and 4 is 4.

The smaller number is 4 and their difference is 4. Their gcd is common,
which we can see is 4.

The gcd didn't change at any step along the way, therefore, the gcd of
the original numbers, 20 and 12 is also 4.

So at each step, we're turning our problem into a smaller problem, 
until we have one we can trivially solve.
This known as the Euclidean algorithm: https://en.wikipedia.org/wiki/Euclidean_algorithm

If the given number have a large difference between them, say 80 and 6,
we'll have to also do a correspondingly larger sequence of subtractions
to get their gcd, which is 2. We'll subtract 6 from the larger 
difference a total of 13 times.

We can find a way of making this process more efficient. Since
repeated subtractions is basically division, we can use the modulus
operator since we're only interested in checking the gcd of the smaller
number and the remainder after dividing the larger number by equal parts.

80 % 6 = 2

Now were interested in the gcd of 6 and 2. We do the same operation
with the smaller numbers

6 % 2 = 0.

Since 2 divides 6 equally, then the gcd of 6 and 2, the same as the 
gcd of 80 and 6 is two.

The general algorithm is as follows: Get the modulus of the two numbers.
As long as the remainder is not zero, repeat the process using the 
previous divisor and the remainder, until the remainder is zero.

The last divisor will be the gcd of the original two numbers.
"""

def gcd(m, n):
    assert m > 0 and n > 0

    r = m % n
    
    while r > 0:
        m, n = n, r
        r = m % n

    return abs(n)



assert gcd(2, 2) == 2
assert gcd(20, 6) == 2
assert gcd(80, 6) == 2
assert gcd(6, 80) == 2
