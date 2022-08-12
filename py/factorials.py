"""
A factorial is a number n such that
n >= 1 and
there exists an integer x >= 0 such that x! = n and
where x = 0, x! = 1 and
where x > 0, x! = x * (x - 1)! and
where n > 1, n % 2 == 0
"""

def test(is_factorial):
    # 1 is always a factorial
    assert is_factorial(1) == True

    # A number less than 1 is not a factorial
    less_than_1 = [0, -1, -4]
    for num in less_than_1:
        assert is_factorial(num) == False

    # Any integer > 1 has to be even to be a factorial
    assert is_factorial(5) == False

    # We can now test with known values
    assert is_factorial(2) == True # 2!
    assert is_factorial(5040) == True # 7!
    assert is_factorial(892) == False
    assert is_factorial(10000) == False


def is_factorial_naive(num):
    """Returns a boolean indicating whether num is a factorial"""

    if num == 1:
        # x = 0 and x! = 1 and (x + 1)! = 1 * 0! = 1
        return True

    if num < 1:
        # x >= 0 and 0! = 1 and x! >= 1
        return False

    if num > 1 and num % 2 != 0:
        # x > 1 and x! > 1 and x! = x * (x - 1) * ... * 2 * 1!
        return False

    # 1! = 1 and x = 1
    x = 1
    fct = 1

    while fct < num:
        # loop invariant: x! = fct and (x - 1)! < num
        x += 1
        fct *= x
        
    
    if fct == num:
        # x! = num
        return True

    # x! > num
    return False


test(is_factorial_naive)
