"""
A simple recursive descent parser for basic arithmetic using
s-expressions (as in lisp).

e.g.

> (+ 1 2)
3

> (/ (* 2 2) 2)
2

> (- 4 3 2)
-1


Note that a language like this uses a prefix (aka Polish) notation 
where the operator precedes its operands.

For example while the infix (conventional) notation would be represented as 

> 3 + 4
7

prefix notation would be represented as

> (+ 3 4)
7

The operator (binary in this scope) is followed by 2 or more operands.

For example

> (+ 3 4 5)
12

is equivalent to the following in infix notation

> (3 + 4) + 5
12

Any additional operand after the first two implies applying the 
operation on the accumulated result from the previous operands with the
additional operand as seen above, until all the operands are exhausted.

We begin by a formal definition of our grammer.

expr              ::= NUM
                  |   form

form              ::= ( operator operands )

operands          ::= expr expr optional_operands
         
optional_operands ::= expr optional_operands | None

operator          ::= +
                  |   -
                  |   *
                  |   /

The definitions on the left are expanded to those on the right.
This reads as:

- An expression is either a number or a form.
- A form is composed of an operator followed by operands enclosed in
  parentheses
- Operands are a pair of expressions followed by an optional operand
- An optional operand is an expression followed by another optional
  operand, or None. This allows us to accept any additional number of
  optional operands
- An operator is one of +, -, /, *

NUM and the operators above are terminal symbols, meaning that they 
cannot be expanded any further. The goal is to expand an expression
(recursively if necessary) until we're have terminal symbols
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
    """Generates tokens identified by the regular expressions above

    Accepts an input string and generates non-whitespace tokens
    If a token is identified as a mismatch, raises an error
    """
    for m in master_pattern.finditer(text):
        token = Token(m.lastgroup, m.group())
        if token.type == "MISMATCH":
            raise RuntimeError(f"Unexpected token {token.value}")
        elif token.type != "WHITESPACE":
            yield token


class Evaluator:
    """Parser for our expressions

    Provides a method `parse` which when given input string,
    parses it and executes it returns a result

    >>> evaluator = Evaluator()
    >>> evaluator.parse("(+ 1 2)")
    3

    Key helper methods that are used:

    _advance - Move forward one token
    _accept  - If the next token is of the given type, advance and 
               return True
    _expect  - Advance expecting the next token to be of the given type
               If it isn't, raise a syntax error
    """

    def parse(self, input_string):
        """Given an input string, evaluate it"""

        self.tokens = generate_tokens(input_string)

        # We have a reference to both the current and next token
        # This allows us to look ahead one token
        self.token, self.next_token = None, None
        self._advance()
        
        # root our grammar is expr
        # call that and return result
        result = self.expr()
        return result

    def expr(self):
        """expr ::= NUM | form
        
        An expression is either number or form"""

        if self._accept("NUM"):
            value = int(self.token.value)
        else:
            # descend into form
            value = self.form()
        return value

    def form(self):
        """form ::= ( operator operands )

        A form is an operator, followed by operands enclosed in parentheses"""

        self._expect("LEFT_PAREN")

        # 'descend' into operator and operands
        operator = self.operator()
        operands = self.operands()

        # operands should be a list of two or more operands
        # apply the operator on the operands
        first, second, *rest = operands
        result = self._apply(operator, first, second)
        for operand in rest:
            result = self._apply(operator, result, operand)
        self._expect("RIGHT_PAREN")

        return result

    def operator(self):
        """operator ::= + | - | * | / """

        if (
                self._accept("PLUS") or
                self._accept("MINUS") or 
                self._accept("TIMES") or 
                self._accept("DIVIDE")
        ):
            return self.token.value
        
        raise SyntaxError("Expected PLUS or MINUS or TIMES or DIVIDE")

    def operands(self):
        """operands ::= expr expr optional_operands
        
        operands are two expressions followed by an optional operand
        """

        # recursively call expression twice
        # Then add optional operands
        first = self.expr()
        second = self.expr()

        return [first, second] + self.optional_operands()
        
    def optional_operands(self):
        """optional_operands ::= expr optional_operands | None
        
        An expression followed by an optional operand, or None
        """
        
        operands = []

        # Check if the next token is the first token of an expression
        # i.e. if token is in FIRST(expr) in parsing terminology
        # If so, collect it and move to the next optional token
        # If not, we have hit the terminal condition (None)

        FIRST_EXPR = ["NUM", "LEFT_PAREN"]  # FIRST(expr)

        if self.next_token.type in FIRST_EXPR:
            operands.append(self.expr())
            operands += self.optional_operands()

        return operands

    def _apply(self, operator, left, right):
        """Applies operator on the left and right operands"""

        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        else:
            result = left / right
        return result

    def _advance(self):
        """Advances one token ahead in input stream"""

        self.token, self.next_token = self.next_token, next(self.tokens, None)

    def _accept(self, token_type):
        """Advances to the next token if it matches the given type"""

        if self.next_token.type == token_type:
            self._advance()
            return True
        return False

    def _expect(self, token_type):
        """Advances to the next token expecting that it is of the given type

        If the token is not of the given type, raises a syntax error
        """

        if not self._accept(token_type):
            raise SyntaxError(f"Expected {token_type}")


evaluator = Evaluator()
assert evaluator.parse("1") == 1
assert evaluator.parse("(+ 1 2)") == 3
assert evaluator.parse("(- 1 2)") == -1
assert evaluator.parse("(* 5 2 3)") == 30
assert evaluator.parse("(/ 10 2)") == 5
assert evaluator.parse("(+ (- 3 5) 2 (- 3 5) 2)") == 0
