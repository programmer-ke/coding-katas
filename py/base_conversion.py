"""
A general procedure that will convert a number from one base to another
where base is between 2 and 36 and number is an integer greater than
or equal to zero i.e.
2 <= base <= 36 and number is in the set of natural numbers.

For representation, we'll use the characters 0-9a-z which will give
us a total of 36 possible characters for each place value. We can
therefore use an ascii string to represent a number of any base with
the most significant to least significant digits arranged left to right.

e.g. '10' to base 10 is the value 10 and the same string to base 2 is
the value 2

The general approach is, given a number of a particular input
representation, find its value and convert it into the expected output
representation.

Characters '0', '1', '2', ... '9' each represents the values 0, 1, 2,
..., 9.  Characters 'a', 'b', 'c', ..., 'z' each represent values 10,
11, 12, ..., 35.

We therefore need a routine to convert from character to value and
vice versa.

TODO:
- Define character conversion routine
"""
