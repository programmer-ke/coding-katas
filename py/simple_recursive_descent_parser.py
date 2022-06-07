"""
A simple recursive descent parser for basic arithmetic using
s-expressions as in lisp.

e.g.

> (+ 1 2)
3

> (/ (* 2 2) 2)
2

> (- 4 3 2)
-1


Note that a language like this uses a prefix (aka Polish) notation 
where the operator precedes it's operands.

For example while the infix (conventional) notation would be represented as 

> 3 + 4
7

Prefix notation would be represented as

> (+ 3 4)
7

The operator (binary in our scope) is followed by 2 or more operands.
For example

> (+ 3 4 5)
12

This is equivalent to the following in infix notation
> (3 + 4) + 5
12

Any additional operand after the first two implies applying the 
operation on the accumulated result from the previous operands with the
additional operand as seen above, until all the operands are exhausted.

We begin by a formal definition of our grammer.

expr     ::= NUM
         |   form

form     ::= ( operator operands )

operands ::= expr expr
         | operands expr

operator ::= +
         |   -
         |   *
         |   /

The definitions on the left are expanded to those on the right.
This reads as:

- An expression is either a number or a form.
- A form is composed of an operator followed by operands enclosed in
  brackets
- An operand is either a pair of expressions, or a set of operands
  followed by an expression. This allows us to have 2 or more operands
  in the form.
- An operator is one of +, -, /, *

NUM and the operators above are terminal symbols, meaning that they 
cannot be expanded any further. The goal is to expand an expression
(recursively if necessary) until we're only left with terminal symbols
that can be evaluated.

More on BNF here: https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form

We then proceed with the implementation below.
"""
import re
import collections

# We define regular expressions to extract the different types of
# tokens from an input string

NUM         = r'(?P<NUM>\d+)'
PLUS        = r'(?P<PLUS>\+)'
MINUS       = r'(?P<MINUS>-)'
TIMES       = r'(?P<TIMES>\*)'
DIVIDE      = r'(?P<DIVIDE>/)'
LEFT_PAREN  = r'(?P<LEFT_PAREN>\()'
RIGHT_PAREN = r'(?P<RIGHT_PAREN>\))'
WHITESPACE  = r'(?P<WHITESPACE>\s+)'
MISMATCH    = r'(?P<MISMATCH>.)'  # a catch all for any patterns we don't expect


# Create a pattern that will match all of the above
master_pattern = re.compile("|".join(
    [NUM, PLUS, MINUS, TIMES, DIVIDE, LEFT_PAREN, RIGHT_PAREN,
     WHITESPACE, MISMATCH]))


# Create a generator for tokens
# We use a namedtuple to create a lightweight class for the tokens
Token = collections.namedtuple("Token", ["type", "value"])

def generate_tokens(text):
    for m in master_pattern.finditer(text):
        token = Token(m.lastgroup, m.group())
        if token.type == "MISMATCH":
            raise SyntaxError(f"Unexpected token {token.value}")
        elif token.type != "WHITESPACE":
            yield token

# todo: evaluator
