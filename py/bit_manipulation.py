def num2bits(num):
    """Return binary string repr of base 10 int"""
    bits = []
    while num:
        bits.append(str(num&0b1))
        num>>=1

    bit_str = "".join(reversed(bits)) if bits else "0"
    return bit_str


def bits2num(bits):
    """Converts binary str or list repr of an int of base 10"""

    num = 0
    #for i, c in enumerate(reversed(bits)):
    #   num += 2**i * int(c)
    for c in bits:
        num <<= 1
        if c == "1":
            num += 1
    return num


def extract_single_num(nums):
    """Return number that occurs singly in nums"""

    # 0 xor num = num
    # num xor num = 0
    result = 0
    for num in nums:
        result ^= num
    return result


assert num2bits(0) == "0"
assert num2bits(1) == "1"
assert num2bits(10) == "1010"
assert num2bits(255) == "11111111"

assert bits2num("0") == 0
assert bits2num("111") == 7
assert bits2num(num2bits(255)) == 255

assert extract_single_num([2]) == 2
assert extract_single_num([3, 5, 8, 4, 5, 3, 8]) == 4

# lshift is essentially multiplying by 2
assert 5<<1 == 10
assert 10<<1 == 20

# rshift is essentially integer divide by 2
assert 10>>1 == 5
assert 5>>1  == 2

# lights analogy
l1 = 0b100 # 4
l2 = 0b010 # 2
l3 = 0b001 # 1

# turn on light 1 and 2
state = l1 | l2
assert state == 6

# check that light 3 is off
assert state & l3 == 0

# turn on light 3
state |= l3

# check that it is on
assert state & l3 == 1

# toggle light 2
state ^= l2

assert state & l2 == 0

# toggle light 2 again
state ^= l2

assert state & l2 == 2
