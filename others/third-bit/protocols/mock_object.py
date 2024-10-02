class Fake:
    def __init__(self, func=None, value=None):
        self.func = func
        self.value = value
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append([args, kwargs])
        if self.func is not None:
            return self.func(*args, **kwargs)
        return self.value


class ContextFake(Fake):
    def __init__(self, name, func=None, value=None):
        super().__init__(func, value)
        self.name = name
        self.original = None

    def __enter__(self):
        assert self.name in globals()
        self.original = globals()[self.name]
        globals()[self.name] = self
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        globals()[self.name] = self.original


def fakeit(name, func=None, value=None):
    assert name in globals()
    fake = Fake(func, value)
    globals()[name] = fake
    return fake


def adder(a, b):
    return a + b


def subber(a, b):
    return a - b


def test_context_no_lasting_effects():
    assert subber(2, 3) == -1
    with ContextFake('subber', value=1234) as fake:
        assert subber(2, 3) == 1234
        assert len(fake.calls) == 1
    assert subber(2, 3) == -1


def test_w_real_function():
    assert adder(2, 5) == 7


def test_w_fixed_return_value():
    fakeit('adder', value=99)
    assert adder(2, 5) == 99

def test_fake_records_calls():
    fake = fakeit("adder", value=99)
    assert adder(2, 3) == 99
    assert adder(3, 4) == 99
    assert adder.calls == [[(2, 3), {}], [(3, 4), {}]]

def test_fake_calculates_result():
    fakeit("adder", func=lambda left, right: 10 * left + right)
    assert adder(2, 3) == 23


def test():
    for k, obj in globals().items():
        if k.startswith('test_'):
            obj()


if __name__ == "__main__":
    test()
