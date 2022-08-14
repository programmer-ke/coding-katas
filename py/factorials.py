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


def is_factorial_naive(num):
    """Returns a boolean indicating whether num is a factorial"""

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


test(is_factorial_naive)
