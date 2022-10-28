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
by elimitating all multiples of two <= n. We repeat the next number in the
sequence, 3, then 5 etc

Infact by eliminating all multiples of whole numbers less than or
equal to the square root of n, we'll have only the prime numbers less
than or equal to n remaining. For example, where n is 30, we only have
to eliminate multiples of 2, 3, 5 which are less than sqrt(30), and
the remaining numbers are primes less than or equal to 30.

This algorithm is known as the Sieve of Eratosthenes:
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

An implementation of it follows. An optimization we'll make is to
only cancel out multiples of each prime from the square of the prime
onwards, because it is guaranteed that any multiples less than the
square of the prime have been cancelled out
"""

def sieve_of_eratosthenes(n):
    """Return primes less than or equal to n

    We use a list who's value at each index specifies
    whether (index + 1) is prime"""

    assert n > 0

    is_prime_list = [True] * n
    _mark_not_prime(is_prime_list, 1)  # 1 is not a prime number

    prev = 1

    while True:
        prime = _get_next_prime(is_prime_list, prev)
        multiple = None if prime is None else prime**2

        if multiple is None or multiple > n:
            # No need for further checks
            break

        while not multiple > n:
            _mark_not_prime(is_prime_list, multiple)
            multiple += prime

        prev = prime

    return [i+1 for i in range(n) if is_prime_list[i]]
    

def _mark_not_prime(is_prime_list, num):
    is_prime_list[num - 1] = False


def _get_next_prime(is_prime_list, prev):
    """Get the next number after prev yet to be marked out"""

    n = len(is_prime_list)
    assert not prev > n

    for i in range(prev, len(is_prime_list)):
        if is_prime_list[i] == True:
            return i+1
    return None  # made explicit

assert sieve_of_eratosthenes(1) == []
assert sieve_of_eratosthenes(2) == [2]
assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]


"""
An issue with this approach is the space requirements relative to the
number of primes upto the number n, because the initial list created 
before marking out non-primes has n elements i.e. a space complexity
of O(n), whereas the final list of primes is much smaller.

For example, on my machine, when n is set to 1e10 (10 to the power 10),
the function above throws a MemoryError exception. When set to a 10th
of that, i.e. 1e9, the function uses 7.4 GB of memory whereas the
resulting list of primes takes up 424 MB.

We also notice with the above algorithm that some numbers will be
marked out more than once. For instance, 30 will be marked out thrice
as a multiple of 2, 3 and 5.

Therefore, two avenues of improving over this algorithm are to reduce
the amount of space required, and to reduce the amount of comparisons
needed to do determine primality.

To determine if a number x is a prime number, it is only necessary to
check if it is divisible by all primes less than or equal to sqrt(x),
because if it is divisible by a composite number, the number already
is itself divisible by a smaller prime number.

We don't need to check for primes > sqrt(x) because they cannot
equally divide x.

This minimises the number of checks for primality per number to the
bare minimum.

To tackle the issue of excessive space used by the previous algorithm,
we'll generate numbers on the fly upto the upper limit n, testing each
for primality, discarding non-primes and retaining only the primes.

An overall algorithm would be like follows.
"""

def generate_primes(n):
    """Return all primes less than or equal to n"""

    assert n > 0

    primes_list = []

    for prime_candidate in _generate_prime_candidates(maxnum=n):
        if _is_prime(prime_candidate, primes_list):
            primes_list.append(prime_candidate)
    return primes_list

"""
When generating candidates for testing for primality, we already know
that any even number greater than 2 is not prime, so we can exclude
even numbers to reduce the number of redundant checks.

Given that x is an odd number, the sequence

x = x + 2 will generate odd numbers
"""

x, l = 3, []
while x < 10:
    l.append(x)
    x += 2
assert l == [3, 5, 7, 9]

"""
Another pattern emerges that we can use to likewise eliminate multiples
of 3, having eliminated multiples of two. The following sequence
has multiples of both 2 and 3 eliminated.

5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, ...

We notice that the next number in the series is generated by either
adding 2 or 4 in an alternating manner. Assigning this to the variable
dx and starting with dx = 2, we can generate the subsequent values for
dx as:

dx = 6 - dx
"""

x, dx = 5, 2
series = []
while x <= 35:
    series.append(x)
    x += dx
    dx = 6 - dx

assert series == [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35]

"""
It may be possible to further optimize this. For example, additionally
eliminating multiples of 5 shows that a different pattern for dx
emerges, but going down this route would make our sequence generator
much more complex.

Using the algorithm above, we can now generate a sequence of candidates
for prime numbers eliminating multiples of 2 and 3. This reduces the
number of unnecessary checks for primality we need to perform.
"""

def _generate_prime_candidates(maxnum):
    """Generates a sequence of number to test for primality

    We skip multiples of 2 and 3"""
    assert maxnum > 0

    if maxnum == 1:
        return []
    if maxnum >= 2:
        yield 2
    if maxnum >= 3:
        yield 3

    candidate = 5
    dx = 2

    while maxnum >= candidate:
        yield candidate
        candidate += dx
        dx = 6 - dx

assert list(_generate_prime_candidates(1)) == []
assert list(_generate_prime_candidates(20)) == [2, 3, 5, 7, 11, 13, 17, 19]


def _is_prime():
    pass
