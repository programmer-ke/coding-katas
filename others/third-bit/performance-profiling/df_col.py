from df_base import DataFrame
from util import all_eq


class DfCol(DataFrame):
    def __init__(self, **kwargs):
        assert len(kwargs) > 0
        assert all_eq(len(kwargs[k]) for k in kwargs)
        for k in kwargs:
            assert all_eq(type(val) for val in kwargs[k])
        self._data = kwargs
    
    def ncol(self):
        return len(self._data)
    
    def nrow(self):
        key = [k for k in self._data.keys()][0]
        return len(self._data[key])

    def cols(self):
        return set(self._data.keys())

    def get(self, col, row):
        assert col in self._data
        assert 0 <= row < len(self._data[col])
        return self._data[col][row]

    def eq(self, other):
        assert isinstance(other, DataFrame)
        for col in self._data:
            if col not in other.cols():
                return False
            for i in range(len(self._data[col])):
                if self._data[col][i] != other.get(col, i):
                    return False
        return True

    def select(self, *names):
        assert all(col in self._data for col in names)
        return DfCol(**{col: self._data[col] for col in names})

    def filter(self, func):
        result = {col: [] for col in self._data}
        for i in range(self.nrow()):
            kwargs = {col: self._data[col][i] for col in self._data}
            if func(**kwargs):
                for col in self._data:
                    result[col].append(self._data[col][i])
        return DfCol(**result)


def test_construct_with_two_pairs():
    df = DfCol(a=[1, 2], b=[3, 4])
    assert df.get("a", 0) == 1
    assert df.get("a", 1) == 2
    assert df.get("b", 0) == 3
    assert df.get("b", 1) == 4


def test_filter():
    def odd(a, b):
        return (a % 2) == 1

    df = DfCol(a=[1, 2], b=[3, 4])
    assert df.filter(odd).eq(DfCol(a=[1], b=[3]))


def test():
    for k, obj in globals().items():
        if k.startswith("test_"):
            obj()


if __name__ == '__main__':
    test()
