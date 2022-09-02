"""
A general procedure that will convert a number from one base to another
where base is between 2 and 36 and number is an integer greater than
or equal to zero i.e.
2 <= base <= 36 and number is in the set of natural numbers.

For representation, we'll use the characters ranges 0-9 and a-z which
will give us a total of 36 possible characters for each place
value. We can therefore use an ascii string to represent a number of
any base with the most significant to least significant digits
arranged left to right.

e.g. '10' to base 10 is the number 10 and to base 2 is the value 2

The general approach is, given a number in a particular input
representation, find its value and convert it into the expected output
representation.

Characters '0', '1', '2', ... '9' each represents the values 0, 1, 2,
..., 9.  Characters 'a', 'b', 'c', ..., 'z' each represent values 10,
11, 12, ..., 35.

We therefore need routines to convert from character to value and
vice versa.
"""

def char2num(char):
    """Returns a number value represented by the character

    char is in the range 0-9a-z"""
    
    # assert char is in the expected ranges
    assert (ord('0') <= ord(char) <= ord('9') or
            ord('a') <= ord(char) <= ord('z'))
    
    num = ord(char) - ord('0')
    if num > 9:
        # in the a-z range
        # skip all the 39 characters btn '9' and 'a' in the ascii range
        num -= 39
    return num

assert char2num('0') == 0
assert char2num('9') == 9
assert char2num('a') == 10
assert char2num('z') == 35

try:
    # should throw an error
    char2num(';')
except Exception as exc:
    assert isinstance(exc, AssertionError)
else:
    assert False, "Failed to raise error"


def num2char(num):
    """Returns char representation of number value

    num is in the range 0-35"""
    assert 0 <= num <= 35

    if num > 9:
        # offset by 39 characters between '9' and 'a' in
        # the ascii range
        num += 39

    char = chr(ord('0') + num)
    return char

assert num2char(0) == '0'
assert num2char(9) == '9'
assert num2char(10) == 'a'
assert num2char(35) == 'z'

try:
    # should throw an error
    num2char(36)
except Exception as exc:
    assert isinstance(exc, AssertionError)
else:
    assert False, "Failed to raise error"
