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
    guess_squared = guess**2
    diff = 1 * (-1 if guess_squared > num else 1)

    while not _close_enough(num, guess_squared, tolerance):
        # loop invariant:
        # guess**2 > num and diff < 0 or guess**2 < num and diff > 0
        # we're converging to num
        guess += diff
        guess_squared = guess**2
        
        if _guess_overshoots_target(num, guess_squared, diff):
            diff = _change_direction(_make_smaller(diff, divisor=10))

    return guess


def _close_enough(num1, num2, threshold):
    return abs(num1 - num2) < threshold


def _guess_overshoots_target(target, actual, direction):
    """Boolean indicating if we've exceeded or subceeded the target

    If we were adding to the guess, we have exceeded the target, 
    and if we were subtracting, we have subceeded it"""
    return (
        (actual > target and direction > 0) or
        (actual < target and direction < 0)
    )


def _change_direction(num): return num * -1


def _make_smaller(num, divisor): return num / divisor


assert square_root_naive(4, initial_guess=2) == 2
assert square_root_naive(16, initial_guess=7) == 4
assert abs(square_root_naive(12, 2) ** 2 - 12) <= 0.0001

"""
With the algorithm above, we see that our initial choice significantly
affects how many iterations it takes to converge to the correct answer.

With each iteration, we modify our guess by a constant amount, and
cannot adjust this by how far away we are from the target.

How can we ensure we take the most efficient route to finding the
best estimate?
"""
