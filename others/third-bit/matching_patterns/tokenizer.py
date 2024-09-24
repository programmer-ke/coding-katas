import string

CHARS = set(string.ascii_letters + string.digits)

class GlobTokenizer:

    def __init__(self):
        self._setup()

    def _setup(self):
        self.result = []
        self.current = ""

    def _add(self, thing):
        if len(self.current) > 0:
            self.result.append(['Lit', self.current])
            self.current = ''
        if thing is not None:
            self.result.append([thing])

    def tok(self, text):
        for char in text:
            if char == "*":
                self._add("Any")
            elif char == "{":
                self._add("EitherStart")
            elif char == ",":
                self._add(None)
            elif char == "}":
                self._add("EitherEnd")
            elif char in CHARS:
                self.current += char
            else:
                raise NotImplementedError(f"Not implemented: {char}")
        self._add(None)
        return self.result


def test_tok_empty_string():
    assert GlobTokenizer().tok("") == []


def test_tok_any_either():
    assert GlobTokenizer().tok("*{abc,def}") == [
        ["Any"],
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"],
    ]


def test():
    for k, obj in globals().items():
        if k.startswith('test_'):
            obj()

test()
