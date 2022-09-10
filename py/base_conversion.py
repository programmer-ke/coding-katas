"""
A general procedure that will convert a number from one base to
another where the base ranges from 2 and 36 and the number is
an integer greater than or equal to zero.

For representation, we'll use the characters ranges 0-9 and a-z which
will give us a total of 36 possible characters for each place
value. We can therefore use an ascii string to represent a number of
any base with the most significant to least significant digits
arranged left to right.

e.g. '10' to base 10 is the number 10 and to base 2 is the value 2

The general approach is, given a number in a particular input
representation, find its value and convert it into the expected output
representation."""

def baseconvert(input_repr, from_base, to_base):
    """Converts number representation between bases"""

    value = get_value(input_repr, from_base)
    output_repr = get_repr(value, to_base)
    return output_repr

"""
Characters '0', '1', '2', ... '9' each represents the values 0, 1, 2,
..., 9.  Characters 'a', 'b', 'c', ..., 'z' each represent values 10,
11, 12, ..., 35.

We will need routines to convert from character to num values and
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


def get_value(num_repr, base):
    """Returns the intrinsic value of the number

    The inputs are the string representation of the number to the
    given base.

    Looking at an example, '125' to base 10 is equivalent to
    (1 * 10^3 + 2 * 10^2 + 5 * 10^0)

    So moving from most significant to least significant characters,
    get the character at that place value, add its value to the
    accumulation so far, and multiply by the base as long as there are
    more significant characters left.

    After doing this for all the characters in the string
    representation, we'll have the accumulation as the sum of the
    value of each character multiplied by the base raised to the
    appropriate power. This is its instrinsic value

    Time complexity of this function depends on length of the
    input number representation because the operations are
    performed per character of the representation.
    """
    assert 2 <= base <= 36
    char_ints = [char2num(char) for char in num_repr]
    assert all([v  < base for v in char_ints])

    acc = 0

    for v in char_ints:
        acc *= base
        acc += v

    return acc


def get_repr(number_value, base):
    """Returns the representation of the number value in the given base

    Say we want to convert 115 to a base 10 representation.
    We'll do so with a sequence of divmod  calculations using the base.
    
    115 divmod 10 = 11, 5
    11 divmod 10 = 1, 1
    1 divmod 10 = 0, 1

    The remainders give us the digit sequence from least to most
    significant.  We stop when the numerator is zero. We'll generalize
    this algorithm for any base 2..36

    The time complexity of this function is log to the given base
    of the number because we divide the number by the base until
    the quotient is zero.
    """
    assert 2 <= base <= 36 and number_value >= 0

    num_repr_reverse = []
    numerator = number_value

    while numerator > 0:
        numerator, remainder = divmod(numerator, base)
        num_repr_reverse.append(remainder)

    # convert from ints to chars and 
    # change to conventional most- to least-significant characters
    num_repr = ''.join(reversed([num2char(n) for n in num_repr_reverse]))
    return num_repr or '0'

"""
The time complexity of `baseconvert` depends on the length of the
input number representation, the number and the base of the output.

If the length of the input is n, the number being x and the output
being y, overall time complexity is
O(n) + O(log(x, y))
"""

def test():
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

    try:
        # should throw an error
        num2char(36)
    except Exception as exc:
        assert isinstance(exc, AssertionError)
    else:
        assert False, "Failed to raise error"

    assert num2char(0) == '0'
    assert num2char(9) == '9'
    assert num2char(10) == 'a'
    assert num2char(35) == 'z'

    assert get_value('15', base=10) == 15
    assert get_value('11', base=2) == 3

    assert get_repr(15, base=10) == '15'
    assert get_repr(3, base=2) == '11'
    assert get_repr(0, base=2) == '0'
    assert get_repr(0, base=36) == '0'

    assert baseconvert('15', from_base=10, to_base=2) == '1111'
    assert baseconvert('15', from_base=10, to_base=3) == '120'
    assert baseconvert('255', from_base=10, to_base=8) == '377'
    assert baseconvert('ff', from_base=16, to_base=2) == '11111111'
    assert baseconvert('0', from_base=36, to_base=2) == '0'
test()
