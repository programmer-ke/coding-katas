"""
A factorial is a number x such that
n! = x, where n is an integer >= 0 and
0! = 1 and
n! = n * (n - 1) * (n - 2) * ... * 0! for n >= 1
"""

def test(is_factorial):
    # 1 is always a factorial
    assert is_factorial(1) == True

    # A number less than 1 is not a factorial
    less_than_1 = [0, -1, -4]
    for num in less_than_1:
        assert is_factorial(num) == False

    # We can now test with known values
    assert is_factorial(2) == True # 2!
    assert is_factorial(5040) == True # 7!
    assert is_factorial(5) == False
    assert is_factorial(892) == False
    assert is_factorial(10000) == False


def is_factorial(num):
    """Returns a boolean indicating whether num is a factorial

    for num > 1!, finds the next factorial >= num. If factorial
    is equal, return True
    """

    if num < 1:
        # n >= 0 and 0! = 1
        return False

    if num == 1:
        # (n = 0 and 0! = 1) or (n = 1 and n! = 1 * !0)
        return True

    # n = 1 and fct = 1! = 1
    n = 1
    fct = 1

    while fct < num:
        # loop invariant: n! = fct and (n - 1)! < num
        n += 1
        fct *= n
        
    
    if fct == num:
        # n! = num
        return True

    # n! > num
    return False


def is_factorial_alt(num):
    """Returns a boolean indicating whether num is a factorial

    Since a factorial is a product of integers > from 1...n,
    where num > 1, dividing by each of 2, 3, 4, ... , n in 
    sequence should result in 1 where num = !n
    
    https://math.stackexchange.com/a/923788
    """

    if num < 1:
        # n >= 0 and 0! = 1
        return False

    if num == 1:
        # (n = 0 and 0! = 1) or (n = 1 and n! = 1 * !0)
        return True

    n = 2

    while num != 1:
        # loop invariant: n >= 2 and num >= 1 and num // n >= 1
        if num % n != 0:
            return False

        num = num // n
        n += 1

    return True


test(is_factorial)
test(is_factorial_alt)
"""
Note that `is_factorial_alt` seems to have a longer running time than
the other for large values of the input where it is a factorial
e.g 10000!

But on average, it would likely detect a non-factorial quicker.

Also, if one already knows the range of the input, the possible factorials
could be pre-computed and cached. The check would then happen in
constant time.
"""
