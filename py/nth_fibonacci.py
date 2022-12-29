"""
Problem: Given a number n, find the nth number in the fibonacci
sequence.

The number n is a positive number greater than zero. The first few
numbers in the sequence are shown in the function below.
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

fn+2 = fn+1 + fn, where n > 0  (formula #0)

We can generate members of the sequence until our desired value of n
"""


def nfib(n):
    """Returns the nth fibonacci number"""

    assert n > 0

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
The time complexity of this approach is O(n), because we have to 
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

f2n = (fn+1)^2 + (fn)^2 (formula #1)

This enables us to generate even placed items in the sequence. To
generate the next 'doubled' number position in the sequence, we'll
need both f2n and f2n+1 as our new fn, fn+1 values in the formula

We find out whether we can represent f2n+1 in terms of n and fn+1
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
f9 = f5^2 + 2*f4*f5

This generalizes to,

f2n+1 = (fn+1)^2 + 2*fn*fn+1 (formula #2)

We can then look at some examples on how we'd use the formulas we have
so far in generating the nth fibonacci number.

A process that involves repeatedly multiplying or dividing by two may
possibly be represented by a sequence of binary digits. So we'll look
at the steps involved in generating our result and compare it with the
binary representation of the number n.

For n = 10 (binary sequence 1010), we find the following steps are
needed after several tries.

| operations                    | explanation                                      | final fn, fn+1 | bin |
-----------------------------------------------------------------------------------------------------------
f1 = 0, f2 = 1                  | Initialization                                   | f1, f2         | 1   |  
f1, f2 -> f2, f3                | Forumlae #1 and #2                               | f2, f3         | 0   |
f2, f3 -> f4, f5 ; f4, f5 -> f6 | Forumlae #1 and #2 then extend seq by 1 using #0 | f5, f6         | 1   |
f5, f6 -> f10, f11 (#1 and #2)  | Forumlae #1 and #2                               | f10, f11       | 0   |


For n = 13 (binary sequence 1101), the following are needed

| operations                          | explanation                                      | next fn, fn+1  | bin |
-----------------------------------------------------------------------------------------------------------------
f1 = 0, f2 = 1                        | Initialization                                   | f1, f2         | 1   |  
f1, f2 -> f2, f3 ; f2, f3 -> f4       | Forumlae #1 and #2 then extend seq by 1 using #0 | f3, f4         | 1   |
f3, f4 -> f6, f7                      | Forumlae #1 and #2                               | f6, f7         | 0   |
f6, f7 -> f12, f13 ; f12, f13 -> f14  | Forumlae #1 and #2 then extend seq by 1 using #0 | f13, f14       | 1   |

If we compare the operations needed to generate the nth fibonacci
number, the following pattern emerges.

- The strategy can be represented by the binary representation of n
  from the most significant bit backwards (as in the last column
  above).
- Initializing fn and fn+1 as f1 and f2 has is associated with a 1
- After initialization, whenever the associated binary digit is an 0,
  we use derived formulae #1 and #2 to get the next fn and fn+1
- Whenever associated binary digit is a 1, we use the formulae #1 and
  #2 and subsequently extend the sequence by 1 using formula #0 to get
  our next fn and fn+1
- In the last iteration, fn becomes our answer

We can use our findings so far to implement our new strategy for
finding the nth fibonacci number.
"""

def nfib(n):
    """Returns the nth fibonacci number

    Approach used:
    - Get the binary representation of n
    - Use the binary representation to execute the strategy
      used to calculate the nth fibonacci number
    """

    assert n > 0
    binary_n = _binary_representation(n)
    return _execute_fibonacci_strategy(binary_n)


def _binary_representation(n):
    """Returns a list representing the binary representation of n"""

    assert n > 0
    
    digits = []

    quotient = n
    
    while quotient > 0:
        quotient, remainder = divmod(quotient, 2)
        digits.append(remainder)
    return list(reversed(digits))


assert _binary_representation(1) == [1]
assert _binary_representation(2) == [1, 0]
assert _binary_representation(13) == [1, 1, 0, 1]

def _execute_fibonacci_strategy(binary_n):
    """Calculate the nth number in the fibonacci sequence

    binary_n is the binary representation of the number n.
    
    Uses the formulae:
    0) fn+2 = fn+1 + fn
    1) f2n = (fn+1)^2 + (fn)^2
    2) f2n+1 = (fn+1)^2 + 2*fn*fn+1

    The rules used are as follows

    - The most significant bit accounts for the initialization
      f1 = 0, f2 = 1
    - Subsequently a '0' in the binary representation means calculating
      the next values for fn and fn+1 using #1 and #2
    - A '1' in the binary representation means calculating the next values
      for fn and fn+1 using #1 and #2 then advancing the sequence by
      1 using #0
    - In the last iteration, fn is our answer
    """
    
    fn, fnplus1 = 0, 1

    for digit in binary_n[1:]:
        # f2n = (fn+1)^2 + (fn)^2
        # f2n+1 = (fn+1)^2 + 2*fn*fn+1
        fnplus1_sq = fnplus1 ** 2
        f2n = fnplus1_sq + fn ** 2
        f2nplus1 = fnplus1_sq + (2 * fn * fnplus1)

        fn, fnplus1 = f2n, f2nplus1
        
        if digit:
            # advance using fn+2 = fn+1 + fn
            fn, fnplus1 = fnplus1, fnplus1 + fn
    
    return fn

test(nfib)

"""
With our second approach, both the space and time complexity are
O(log(n)). This is because we use the binary representation of n to
execute our computation strategy, which is in the order of log(n, 2).
"""
