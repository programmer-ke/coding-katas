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

"""
For a large number m, less than or equal to n, we'll be doing
almost m checks to identify if it is a prime number. Also, we'll have
to do this for all numbers from 2 to n.

Two avenues of improving over this are to either decrease the numbers
we have to test for primality, or decrease the number of checks per
number to determine primality.

Taking the first approach, we know 2 is a prime number, we can start
by elimitating all factors of two <= n. We repeat the next number in the
sequence, 3, then 5 etc

Infact by eliminating all multiples of whole numbers less than or
equal to the square root of n, we'll have only the prime numbers less
than or equal to n remaining. For example, where n is 30, we only have
to eliminate multiples of 2, 3, 5 which are less than sqrt(30), and
the remaining numbers are primes less than or equal to 30.

This algorithm is known as the Sieve of Eratosthenes:
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

We can implement an algorithm similar the above:
"""
