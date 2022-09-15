"""
Problem: Given a positive number, calculate its square root

One approach is making a series of guesses until we get the
correct answer (or one that is close enough).

For example, when calculating the square root of 12, we can
start with a guess of 4, decrementing by 1 until we find the
next one who's square is less than or equal to 12.

4^2 = 16
3^2 = 9

We then increment by a smaller number, say 0.1 until we find
one who's square is greater than or equal to 12.

3.1^2 = 9.61
3.2^2 = 10.24
3.3^2 = 10.89
3.4^2 = 11.55
3.5*2 = 12.25

We subtract yet a smaller number from 3.5 e.g. 0.01 and repeat the
procedure until we find a number whose square is close enough to 12
for our needs. An algorithm for this will look like the one below.
"""

def square_root_naive(num, initial_guess):
    """Find the square root of num using initial_guess as starting point"""

    assert num > 0 and initial_guess > 0

    # We can tolerate an error of at most 0.0001
    tolerance = 0.0001
    guess = initial_guess
    diff = 1 * (-1 if guess**2 > num else 1)

    while abs(num - guess**2) > tolerance:
        # loop invariant:
        # guess**2 > num and diff < 0 or guess**2 < num and diff > 0
        guess += diff

        if (guess**2 > num and diff > 0) or (guess**2 < num and diff < 0):
            # change sign of diff and divide by 10
            diff = (diff * 0.1) * -1

    return guess

assert square_root_naive(4, 2) == 2
assert square_root_naive(16, 7) == 4
assert abs(square_root_naive(12, 2) ** 2 - 12) <= 0.0001
