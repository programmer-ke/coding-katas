"""
Problem: Given a number n, return the nth number in the fibonacci
sequence.

The number n is a positive number greater than zero. The first few
numbers in the sequence are:
"""

def test(nfib):
    assert nfib(1) == 0
    assert nfib(2) == 1
    assert nfib(3) == 1
    assert nfib(4) == 2
    assert nfib(5) == 3
    assert nfib(6) == 5

"""
The value of n is supplied to the function `nfib`.

The straight forward approach is to generate numbers in the fibonacci
sequence until we get the nth number and return that.

Initializing the first two numbers numbers as:

f1 = 0, f2 = 1 and using the formula

fn+2 = fn+1 + fn, where n > 0

We can generate members of the sequence until our desired value of n
"""


def nfib(n):
    """Return the nth fibonacci number"""

    if n == 1:
        return 0
    if n == 2:
        return 1

    i = 3
    fnplus1, fn = 1, 0

    while i <= n:
        fnplus2 = fnplus1 + fn

        fnplus1, fn = fnplus2, fnplus1
        i+=1

    return fnplus2

test(nfib)

"""
This time complexity of this approach is O(n), because we have to 
generate all the fibonacci numbers in sequence until we reach our
desired nth fibonacci number.

We can explore whether there's a better mechanism for generating the
nth fibonacci number without using the two terms preceeding it in the
sequence.

We can check whether it's possible to the generate the nth number
by a doubling of terms in some way instead of mere addition. For
example, can we represent f8 in terms of f4 and f5?

Using the standard formula:

f8 = f7 + 76
f7 = f6 + f5
f6 = f5 + f4

Therefore,

f8 = ((f5 + f4) + f5) + (f5 + f4)

f8 = 3f5 + 2f4

But we find that f5 = 3 and f4 = 2. Therefore,

f8 = f5 * f5 + f4 * f4

f8 = f5^2 + f4^2

By checking a few examples, we find that this generalizes to other
numbers in the sequence

f2n = (fn+1)^2 + fn^2

This enables us to generate even placed items in the sequence. To
generate the next 'doubled' number position in the sequence, we'll
need f2n and f2nplus1.

We find out whether we can represent f2nplus1 in terms of n and fnplus1
e.g. f9 in terms of f4 and f5.

f9 = f8 + f7
f8 = f7 + f6
f7 = f6 + f5
f6 = f5 + f4

Therefore,

f9 = (((f5 + f4) + f5) + (f5 + f4)) + ((f5 + f4) + f5)
f9 = 5f5 + 3f4

We know that f5 = 3 and f4 = 2. Therefore,

f9 = 3f5 + 2f5 + 3f4
f9 = f5^2 + f4*f5 + f5*f4
f9 = f5^2 + 2f4f5

This generalizes to,

f2n+1 = (fn+1)^2 + 2*fn*fn+1

todo: examples
"""
