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
import math

def square_root_naive(num, initial_guess):
    """Find the square root of num using initial_guess as starting point"""

    assert num > 0 and initial_guess > 0

    # We can tolerate an error less than 0.000001
    tolerance = 1e-6
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


assert square_root_naive(4, initial_guess=2) == math.sqrt(4)
assert square_root_naive(16, initial_guess=7) == math.sqrt(16)
assert math.isclose(square_root_naive(12, 2), math.sqrt(12), rel_tol=1e-6)


"""
With the algorithm above, we see that our initial choice significantly
affects how many iterations it takes to converge to the correct
answer.

With each iteration, we modify our guess by a constant amount. We
cannot adjust this by how far away we are from the target, e.g. by
making larger jumps when we're further off and smaller jumps when
we're nearer to the target.

How can we ensure we take the most efficient route to finding the best
estimate?

Let's say we want the square root of 20. We select 10 as our guess.

10 * 10 = 100

This is way off from 20. We divide 20 by 10 to get its complementary
value which is 2, and 2 * 2 = 4.

So 10 is on one extreme from the square root of 20 and 2 is on the
other.

The square root is somewhere between 2 and 10. We therefore determine
the average of those two and use that as our next guess.

(10 + 2)/2 = 6

6 * 6 = 36

36 is now closer to 20, but still way off. If we divide 30 by 6 we get
3.3333 as its complementary value and 3.3333 * 3.333 =~ 11.1111

The square root of 20 is therefore somewhere between 6 and 3.3333 and
so we check the average of the two again.

(6 + 3.333)/2 = 4.6666

4.6666 * 4.6666 = 21.7777

Our guess is now getting closer to the square root of 20.

10 -> 6 -> 4.6666 -> ...

The trend shows that we're converging to the square root of 20. We can
repeat the same process iteratively until there is no significant
change in our guess. This means that we are very close to the square
root of our target, and can therefore use the latest guess as its
square root.

For our purposes, we can stop when the difference between the previous
guess and the latest guess is less than 0.0001 i.e.

abs(latest_guess - prev_guess) < 0.0001
"""

def square_root_improved(target):
    """Calculates the square root of the target"""

    assert target > 0

    tolerance = 1e-6
    latest_guess = target / 2

    while True:
        prev_guess = latest_guess
        latest_guess = ((target / prev_guess) + prev_guess) / 2
        if _close_enough(latest_guess, prev_guess, tolerance):
            break
        
    return latest_guess

assert square_root_improved(4) == math.sqrt(4)
assert math.isclose(square_root_improved(16), math.sqrt(16))
assert math.isclose(square_root_improved(0.02), math.sqrt(0.02))
