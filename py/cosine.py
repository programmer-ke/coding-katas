"""
Implementing Cosine using the Taylor series
*******************************************

## Problem Definition

Implementing function cos(x) defined by the infinite series

cos(x) = 1 - (x^2)/2! + (x^4)/4! - (x^6)/6! + ...

Acceptable error for computation is 10^-6

## Approach

Starting from 1, we add/subtract terms in the given series to some
point, otherwise the algorithm will never terminate.

We therefore use the acceptable error as a threshold for termination
i.e.  when the additional term contributes a value less than the 10^-6
we stop.

Each term after 1 in the series can be described as

(x^i)/i! for i in the series 2, 4, 6, 8, ...

We also note that the sign alternates with each additional term in the
sequence in following way:

sign = -sign

A simple implementation would be to start with 1, then with each
additional term, negate the sign and calculate (x^i)/i! and add to
the previous term.

Each term (x^i)/i! can be calculated in a manner like below:
"""

def calculate_term(x, i):
    """x^i/i!"""
    term = 1
    for n in range(1, i+1):
        term *= x / n

    return term

assert calculate_term(1, 2) == 1/2                    # 1^2/2!
assert calculate_term(2, 4) == 2**4 /(4 * 3 * 2 * 1)  # 2^4/4!
        
"""
However, we notice some repeated computations for each additional term
i.e.
Computing x^6/6! includes computation for x^4/4! which includes
computation for x^2/2!.

So with each additional term, time complexity for computation grows
linearly.

We can look for opportunities to make this constant for each additional
term, by looking at ways of expressing the next term in the series
in terms of the previous one:

base case = 1
1st term: x^2/2! = x/2 * x/1 * 1      = x^2/(2 * 1) * base case
2nd term: x^4/4! = x/4 * x/3 * x^2/2! = x^2/(4 * 3) * 1st term
3rd term: x^6/6! = x/6 * x/5 * x^4/4! = x^2/(6 * 5) * 2nd term
... and so forth.

We can therefore represent the a subsequent term in the series in terms
of the previous term as:

x^i/i! = (x^2/i*(i-1)) * previous term

Time complexity for each additional time now remains constant.

Putting all the above together, our general approach is to start
with 1 as our base term, then iteratively generate each additional
term negating the sign and adding it to the previous. We do this until
the absolute value is less than the acceptable error of 10^-6.
At this point, the sum of terms will be an accurate enough cosine of
our input.
"""

import math

def main():
    inputs = [-1, 0, 1]
    for x in inputs:
        assert math.isclose(math.cos(x), cosine(x), rel_tol=1e-06)


def cosine(x):
    """Returns the cosine of x to an acceptable error of 10^-6

    Uses the taylor series, but refactored:
    cos(x) = 1 - (x^2)/2! + (x^4)/4! - (x^6)/6! + ...
    """

    y = 0
    term = 1
    i = 0  # holds next in the series 0, 2, 4, 6, ...
    x2 = x * x  # x^2 is constant in each iteration

    while abs(term) > 1e-06:
        # loop invariant:
        # for iteration j, i = 2j and y = sum of first j terms in series
        y += term
        i += 2
        term = -(x2 / (i * (i - 1)) * term)
    return y

main()
