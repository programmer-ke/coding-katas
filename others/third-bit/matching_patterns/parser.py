from glob import Lit, Any, Either, Null
from tokenizer import GlobTokenizer


class GlobParser:

    def parse(self, token_string):
        tokenizer = GlobTokenizer()
        tokens = tokenizer.tok(token_string)
        tree = self._parse(tokens)
        return tree

    def _parse(self, tokens):
        if not tokens:
            return Null()

        front, back = tokens[0], tokens[1:]

        match front[0]:
            case 'Any':
                handler = self._parse_Any
            case 'EitherStart':
                handler = self._parse_EitherStart
            case 'Lit':
                handler = self._parse_Lit
            case _:
                raise ValueError(f'Unknown token type: {front}')

        return handler(front[1:], back)

    def _parse_Any(self, rest, back):
        return Any(self._parse(back))

    def _parse_Lit(self, rest, back):
        return Lit(rest[0], self._parse(back))

    def _parse_EitherStart(self, rest, back):
        if (
            len(back) < 3
            or back[0][0] != "Lit"
            or back[1][0] != "Lit"
            or back[2][0] != "EitherEnd"
        ):
            raise ValueError(f"badly formatted Either: {back[:3]}")
        
        left = Lit(back[0][1])
        right = Lit(back[1][1])
        return Either(left, right, self._parse(back[3:]))
                

def test_parse_either_two_lit():
    assert GlobParser().parse("{abc,def}") == Either(
        Lit("abc"), Lit("def")
    )


def test_parsing_examples():
    samples = (
        ("*", Any()),
        ("a*b", Lit("a", Any(Lit("b")))),
        (
            "{doom,year}*{2020,2024}",
            Either(Lit("doom"), Lit("year"), Any(Either(Lit("2020"), Lit("2024")))),
        ),
    )

    for glob, matchers in  samples:
        results = GlobParser().parse(glob)
        assert  results == matchers

def test_matching():
    samples = (
        ('*', 'foobar'),
        ('a*b', 'abb'),
        ('a*b', 'ab'),
        ('{a,b}', 'b'),
    )

    for glob, target in samples:
        matchers = GlobParser().parse(glob)
        assert matchers.match(target)
    
def test():
    for k, value in globals().items():
        if k.startswith('test_'):
            value()


if __name__ == "__main__":
    test()
