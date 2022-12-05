"""
Problem: Generate all the prime numbers in the first n positive
integers

A prime number is divisible only by 1 and itself. Therefore, the
obvious approach to identify a prime number is to test if it is
divisible by any number between one and itself.
"""


def is_prime(num):
    assert num > 1

    for i in range(2, num):
        if num % i == 0:
            return False
    return True


assert is_prime(2) == True
assert is_prime(13) == True
assert is_prime(15) == False
assert is_prime(103) == True
assert is_prime(1000) == False


"""
For a large number m, less than or equal to n, we'll be doing almost m
checks in some cases to identify if it is a prime number. We also
have to do this for all numbers from 2 to n.

Two avenues of improving over this are to decrease the numbers
we have to test for primality and decrease the number of checks per
number to determine primality.

Taking the first approach, we know 2 is a prime number, we can start
by eliminating all multiples of two <= n. We repeat the next number in
the sequence, 3, then 5 etc

Infact by eliminating all multiples of whole numbers <= the square
root of n, we'll have only the prime numbers <= n left. For example,
where n is 30, we only have to eliminate multiples of 2, 3, 5 which
are <= sqrt(30), and the remaining numbers are primes less than or
equal to 30.

This algorithm is known as the Sieve of Eratosthenes:
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

It can be implemented as follows.
"""


def sieve_of_eratosthenes(n):
    """Return primes less than or equal to n

    We use a list as a sieve who's boolean value at each index
    specifies whether (index + 1) is prime after eliminating
    all multiples of primes <= sqrt(n)"""

    assert n > 0

    is_prime_list = [True] * n
    _mark_not_prime(is_prime_list, 1)  # 1 is not a prime number

    prev = 1

    while True:
        prime = _get_next_prime(is_prime_list, prev, list_length=n)
        # An optimization possible here is that we only need to cancel
        # multiples starting from the square of the prime number
        multiple = None if prime is None else prime**2

        if multiple is None or multiple > n:
            # No need for further checks
            break

        while not multiple > n:
            _mark_not_prime(is_prime_list, multiple)
            multiple += prime

        prev = prime

    for i, is_prime in enumerate(is_prime_list):
        if is_prime:
            yield i + 1


def _mark_not_prime(is_prime_list, num):
    is_prime_list[num - 1] = False


def _get_next_prime(is_prime_list, prev, list_length):
    """Get the next number after prev yet to be marked out"""

    assert not prev > list_length

    for i in range(prev, list_length):
        if is_prime_list[i] == True:
            return i + 1

    # no primes left
    return None


assert list(sieve_of_eratosthenes(1)) == []
assert list(sieve_of_eratosthenes(2)) == [2]
assert list(sieve_of_eratosthenes(10)) == [2, 3, 5, 7]


"""
An issue with this approach is the excessive space requirements
relative to the number of primes upto the number n. The initial list
created before marking out non-primes has n elements i.e. a space
complexity of O(n), whereas the actual number of primes in the list is
much smaller.

For example, on my machine, when n is set to 1e10 (10 to the power
10), the function above throws a MemoryError exception. When set to a
10th of that, i.e. 1e9, the algorithm uses upto 9.3 GB of memory to
complete, while the resulting list of primes uses only 424 MB.

We also notice with the above algorithm that some numbers will be
marked out more than once. For instance, 30 will be marked out thrice
as a multiple of 2, 3 and 5.

Two possible approaches to improving over the sieve algorithm are to
reduce the amount of space required, and to reduce the amount of
comparisons needed to do determine primality.

In general, to determine if a number x is a prime number, it is only
necessary to check if it is divisible by all primes less than or equal
to sqrt(x), because if it is divisible by a composite number, the
number already is itself divisible by a smaller prime number.

We don't need to check for primes > sqrt(x) because they cannot equally
divide x.

This minimises the number of checks for primality per number to the
bare minimum.

To tackle the issue of excessive space used by the previous algorithm,
we'll generate numbers on the fly upto the upper limit n, testing each
for primality, discarding non-primes and retaining only the primes.

An overall algorithm would be like follows.
"""
import math


def generate_primes_v1(n):
    """Return all primes less than or equal to n

    All prime numbers upto n are indivisible by all
    prime numbers <= sqrt(n)

    Our candidate generator skips multiples of 2 and 3 from 5 onwards,
    so we only need test each candidate with primes starting from 5
    """

    assert n > 0

    prime_divisors, num_divisors = [5], 1
    sqrt_n = math.sqrt(n)

    for prime_candidate in _generate_prime_candidates(maxnum=n):

        if prime_candidate in (2, 3, 5):
            yield prime_candidate
            continue

        if _is_prime(prime_candidate, prime_divisors, num_divisors):
            yield prime_candidate

            if prime_candidate <= sqrt_n:
                prime_divisors.append(prime_candidate)
                num_divisors += 1


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
Another pattern emerges that we can use to likewise eliminate
multiples of 3, having eliminated multiples of two. The following
sequence has multiples of both 2 and 3 eliminated.

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
number of primality checks we need to perform by more than a half.
"""


def _generate_prime_candidates(maxnum):
    """Generates a sequence of number to test for primality

    We skip multiples of 2 and 3"""
    assert maxnum > 0

    if maxnum == 1:
        return
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

"""
Final piece of this approach is to determine whether a prime candidate
is a prime number.
"""


def _is_prime(candidate, prime_divisors, num_divisors):
    """Returns a boolean indicating whether the candidate is prime

    The candidate is prime if it is indivisible by any prime number
    less than or equal to its square root"""

    # We should provide prime divisors for any candidate
    # that is not the first prime number
    assert candidate == 2 or num_divisors > 0

    if candidate == 2:
        return True

    sqrt_candidate = math.sqrt(candidate)
    index = 0

    while index < num_divisors and prime_divisors[index] <= sqrt_candidate:
        rem = candidate % prime_divisors[index]
        if rem == 0:
            return False
        index += 1

    return True


assert _is_prime(2, [], num_divisors=0) == True
assert _is_prime(6, [2, 3, 5], num_divisors=3) == False
assert _is_prime(23, [2, 3, 5], num_divisors=3) == True

"""
At this point we have completed the prime generate and can run a few
tests.
"""


def test_generating_primes(func):
    assert list(func(1)) == []
    assert list(func(2)) == [2]
    assert list(func(7)) == [2, 3, 5, 7]
    assert list(func(10)) == [2, 3, 5, 7]
    assert list(func(25)) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
    assert list(func(1000)) == list(sieve_of_eratosthenes(1000))


test_generating_primes(generate_primes_v1)


"""
Comparing the two mechanisms we have so far on generating prime
numbers, I find on my machine that the sieve of eratosthenes
(10.329625175998444 seconds) is faster than the latter approach
(12.171041731000514 seconds).
"""

# To measure and compare the approaches, invoke script with argument 't'
import sys

TIMING_MODE = True if (len(sys.argv) > 1 and sys.argv[1] == "t") else False
if TIMING_MODE:
    import timeit

    no_iterations = 10000
    print("timing sieve_of_eratosthenes")
    print(
        min(
            timeit.Timer(
                "list(sieve_of_eratosthenes(1000))", globals=globals()
            ).repeat(5, no_iterations)
        )
    )
    print("timing generate_primes_v1")
    print(
        min(
            timeit.Timer(
                "list(generate_primes_v1(1000))", globals=globals()
            ).repeat(5, no_iterations)
        )
    )

"""
The problem with the sieve of eratosthenes is that the prime
candidates list grows proportionally with n, and for large values of
n, we run out of space.

We next explore ways of optimizing v1. We notice that whenever we're
testing a candidate for primality, we calculate its square root. This
adds to the time complexity of testing each candidate.

Since we only need to test a candidate with a prime number less than or
equal to its square root, we notice the following relationship between
the range of values for the candidate and the prime number divisors
needed to determine primality.

candidate x  | prime divisors
-------------------------------
3<=x<9       | 2
9<=x<25      | 2, 3
25<=x<49     | 2, 3, 5
49<=x<121    | 2, 3, 5, 7

Therefore, starting with maximum prime divisor as 2, we only advance
it to the 3 if the candidate equals or exceeds the square of 3, then
advance it to 5 if the candidate equals or exceeds the square of 5 and
so forth.

We can then replace the square root calculation with a check that
conditionally advances our max prime divisor in the divisors list
based on the value of the candidate.

We'll modify the parent function slightly to maintain state of the
current index of the max prime divisor, incrementing it as necessary,
and passing it to the prime tester helper function.
"""


def generate_primes_v2(n):
    """Return all primes less than or equal to n

    All prime numbers upto n are indivisible by all
    prime numbers <= sqrt(n)
    """

    assert n > 0

    prime_divisors, num_divisors = [5], 1
    max_divisor_index, divisors_candidate_limit = 0, 49
    sqrt_n = math.sqrt(n)

    for prime_candidate in _generate_prime_candidates(maxnum=n):

        if prime_candidate in (2, 3, 5):
            yield prime_candidate
            continue

        if (
            prime_candidate >= divisors_candidate_limit
            and max_divisor_index + 1 < num_divisors
        ):
            # Include next prime divisor in testing
            max_divisor_index += 1

            if max_divisor_index + 1 < num_divisors:
                # Set the next upper limit for candidate with current prime divisors
                divisors_candidate_limit = (
                    prime_divisors[max_divisor_index + 1] ** 2
                )

        if _is_prime(
            prime_candidate, prime_divisors, max_divisor_index, num_divisors
        ):
            yield prime_candidate

            if prime_candidate <= sqrt_n:
                prime_divisors.append(prime_candidate)
                num_divisors += 1


"""
We then modify the prime tester function to make use of the maximum divisor
index instead of square root of candidate.
"""


def _is_prime(candidate, prime_divisors, max_divisor_index, num_divisors):
    """Returns a boolean indicating whether the candidate is prime

    The candidate  is prime if it  is indivisible by any the prime
    divisors less than or equal to its square root

    max_divisor_index will indicate where the max prime number used
    for testing is in the prime_divisors list"""

    assert num_divisors > max_divisor_index

    for i in range(max_divisor_index + 1):
        rem = candidate % prime_divisors[i]
        if rem == 0:
            return False

    return True


test_generating_primes(generate_primes_v2)


"""
This version shows the best performance so far in generating primes
(9.930310007999651 seconds).
"""
if TIMING_MODE:
    print("timing generate_primes_v2")
    print(
        min(
            timeit.Timer(
                "list(generate_primes_v2(1000))", globals=globals()
            ).repeat(5, no_iterations)
        )
    )

"""
One potentially expensive operation being performed per prime
candidate is the modulus operation, which is in essence a division
operation. Division is an relatively [expensive operation][1] and so
eliminating this may possibly improve the performance of the
algorithm.

[1]: https://stackoverflow.com/q/15745819

A clue we can get from the sieve of eratosthenes is that we only need
to eliminate multiples of all primes <= sqrt(n) when generating all
primes <= n.

Inspired by the sieve, we can decide to keep track of multiples of
prime numbers that we can use to test against the candidate but
discard any discovered non-primes to avoid the excessive cost in space.

If the candidate is a multiple of any of the relevant prime numbers,
we discard it and move on to the next candidate. Otherwise, we add it
to the list of prime numbers.

Compared to the sieve algorithm, we use significantly less storage as
all non-primes are discarded. Compared to our latest implementation,
we incur an additional cost of space; multiples of primes to be tested
against the candidate, but this helps us avoid the modulus operation.

The following table shows, for each range of candidate x, the prime
testers used, and their corresponding multiples. We notice that for
each prime divisor, its starting multiple used for prime number
testing is its square.


candidate x  | prime testers  | corresponding multiples
-------------------------------------------------------
3<=x<9       | 2              | 4+
9<=x<25      | 2, 3           | 10+, 9+
25<=x<49     | 2, 3, 5        | 26+, 27+, 25+
49<=x<121    | 2, 3, 5, 7     | 50+, 51+, 50+, 49+

Since our candidate generator does not generate multiples of 2 and 3,
we can exclude them from the prime testers list.
"""


def generate_primes_v3(n):
    """Return all primes less than or equal to n

    All prime numbers upto n are indivisible by all
    prime numbers <= sqrt(n)
    """

    assert n > 0

    prime_testers, num_testers = [5], 1
    max_tester_index, testers_candidate_limit = 0, 49
    prime_multiples = [prime_testers[max_tester_index] ** 2]
    sqrt_n = math.sqrt(n)

    for prime_candidate in _generate_prime_candidates(maxnum=n):

        if prime_candidate in (2, 3, 5):
            yield prime_candidate
            continue

        if (
            prime_candidate >= testers_candidate_limit
            and max_tester_index + 1 < num_testers
        ):
            # Include next prime tester in testing
            max_tester_index += 1
            prime_multiples.append(prime_testers[max_tester_index] ** 2)

            if max_tester_index + 1 < num_testers:
                # Set the next upper limit for candidate with current prime testers
                testers_candidate_limit = (
                    prime_testers[max_tester_index + 1] ** 2
                )

        if _is_prime(
            prime_candidate,
            prime_testers,
            prime_multiples,
            max_tester_index,
            num_testers,
        ):
            yield prime_candidate

            if prime_candidate <= sqrt_n:
                prime_testers.append(prime_candidate)
                num_testers += 1


def _is_prime(
    candidate, prime_testers, prime_multiples, max_tester_index, num_divisors
):
    """Returns a boolean indicating whether the candidate is prime

    The candidate  is prime if it  is indivisible by any the prime
    numbers less than or equal to its square root.

    We determine this by checking that the candidate is not equal
    to any multiples of these prime numbers.

    max_tester_index will indicate the where the max prime number we
    use for testing is in the prime_testers list"""

    _validate_tester_input(
        candidate, num_divisors, max_tester_index, prime_multiples
    )

    # test for primality
    for i in range(max_tester_index + 1):

        while prime_multiples[i] < candidate:
            # increment by prime number doubled to skip
            # multiples of 2
            prime_multiples[i] += prime_testers[i] * 2

        if prime_multiples[i] == candidate:
            return False

    return True


def _validate_tester_input(
    candidate, num_divisors, max_tester_index, prime_multiples
):
    assert candidate > 1
    assert num_divisors > max_tester_index
    try:
        prime_multiples[max_tester_index]
    except IndexError:
        msg = "Number of multiples is less than number of prime testers"
        raise AssertionError(msg)


test_generating_primes(generate_primes_v3)

if TIMING_MODE:
    print("timing generate_primes_v3")
    print(
        min(
            timeit.Timer(
                "list(generate_primes_v3(1000))", globals=globals()
            ).repeat(5, no_iterations)
        )
    )

"""
Version 3 (12.78460630399968 seconds) compares unfavourably to the
previous version.  We can conclude that the time complexity of
maintaining prime multiples to test prime candidates is greater than
the modulus operation being performed per candidate. This behaviour
may be dependant on the particular computer architecture since
division may be implemented in different ways.

With version 3 of the modified sieve algorithm, we update multiples of
primes if necessary for each prime candidate. We do this by iterating
through the list of multiples.

Suppose we could hold all the multiples as keys in a dictionary, to
check whether a candidate is prime by a membership test in the
dictionary which is practically an O(1) (constant) time operation.

The value of an item in the dictionary is the prime number
corresponding to the multiple. If the candidate is missing from the
dictionary, we conclude it's a prime number and initialize its first
multiple in the dictionary as its square.

If it exists in the dictionary, we know that it is not prime. At this
point, we calculate and set the next multiple associated with the
prime number to be used for testing against a future candidate. We can
then delete the dictionary item associated with the current multiple
since we no longer have any use for it. This means that the space
complexity will peak at O(m), where m = sqrt(n), n is our maximum
number.

An issue then emerges where some primes will share multiples. We can
work around this by incrementing the multiple associated with the
prime number until we find a unique one, and add that to the
dictionary.

A simple optimization we can make is to skip multiples of 2, because
all even numbers are non-primes. The square of an odd number will
always be odd e.g. 3 * 3 = 9, 5 * 5 = 25, 11 * 11 = 121

We'll increment the multiples by double the prime number to skip the
even multiples. The sum of and odd number and an even number will
always be odd. For example, the multiples of 3 and 5 will be
incremented in the following sequences as we add increment by double
the prime.

3: 9, 15, 21, 27, 33, 39, ...
5: 25, 35, 45, 55, 65, 75, ...
"""


def generate_primes_v4(n):
    """Generate all prime numbers <= n

    multiples dict holds key=> value pairs of multiple => prime
    """

    assert n > 0

    multiples = {}
    candidate = 2
    sqrt_n = math.sqrt(n)

    while not candidate > n:

        if candidate == 2:
            yield candidate
            candidate += 1
            continue

        if _is_prime(candidate, multiples):
            yield candidate
            if not candidate > sqrt_n:
                multiples[candidate * candidate] = candidate

        else:
            current_multiple = candidate
            _set_next_unique_multiple(current_multiple, multiples)
            del multiples[current_multiple]

        candidate += 2


def _is_prime(candidate, multiples):
    return candidate not in multiples


def _set_next_unique_multiple(multiple, multiples):

    prime_factor = multiples[multiple]
    while multiple in multiples:
        multiple += prime_factor * 2
    multiples[multiple] = prime_factor


test_generating_primes(generate_primes_v4)

if TIMING_MODE:
    print("timing generate_primes_v4")
    print(
        min(
            timeit.Timer(
                "list(generate_primes_v4(1000))", globals=globals()
            ).repeat(5, no_iterations)
        )
    )

"""
This version of the modified sieve turns out to be the fastest overall
(8.464073090000966 seconds).

By generating numbers on the fly, it avoids storage cost of O(n) for
generating primes upto n as in the standard sieve of eratosthenes
implementation. The storage cost will be O(sqrt(n)) because we're only
storing unique multiples of prime numbers <= sqrt(n).

The determination of whether a number is prime now takes constant time
because it's now simply a membership test in a python dict, which has
O(1) lookup time. This is in contrast to comparing a candidate with
a list of primes, or multiple of primes as in the previous versions.

We now have a prime number generator that generates primes with a
reasonably well enough time and space complexity. However, there are
other theoretically faster sieves for generating primes e.g. the 
Atkins Sieve.

References
---------
https://en.wikipedia.org/wiki/Generation_of_primes
https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
https://code.activestate.com/recipes/117119-sieve-of-eratosthenes/
"""
