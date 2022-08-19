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

We also not that the sign alternates with each additional term in the
following way with each additional sequence

sign = -sign

A simple implementation would be to start with 1, then with each
additional term, negate the sign and calculate (x^i)/i! and add to
the previous term.

Each term (x^i)/i! can be calculated in a manner like below:
"""

def calculate_term(x, i):
    term = 1
    for n in range(1, i+1):
        term *= x / n

    return term

assert calculate_term(1, 2) == 1/2                # 1^2/2!
assert calculate_term(1, 4) == 1/(4 * 3 * 2 * 1)  # 1^4/4!
        
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

We can therefore represent the a subsequent term in the series as
x^i/i! = (x^2/i*(i-1)) * previous term
"""
