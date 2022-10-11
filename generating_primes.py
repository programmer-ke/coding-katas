"""
Problem: Generate all the prime numbers in the first n positive
integers

A prime number is divisible only by 1 and itself. Therefore, one
approach to identify a prime number is to test if it is divisible by
any number between one and itself.
"""

def is_prime(num):
    assert num > 1

    for i in range(2, num):
        if num % i == 0:
            return False
    return True


def test_is_prime(is_prime_func):
    assert is_prime_func(2) == True
    assert is_prime_func(13) == True
    assert is_prime_func(15) == False
    assert is_prime_func(103) == True
    assert is_prime_func(1000) == False

test_is_prime(is_prime)
