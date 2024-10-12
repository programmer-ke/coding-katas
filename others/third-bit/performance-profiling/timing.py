import time

from df_col import DfCol
from df_row import DfRow

RANGE = 10



def make_col(nrow, ncol):
    def _col(n, start):
        return [((start + i) % RANGE) for i in range(n)]
    fill = {f"label_{c}": _col(nrow, c) for c in range(ncol)}
    return DfCol(**fill)

def make_row(nrow, ncol):
    labels = [f"label_{c}" for c in range(ncol)]
    def _row(r):
        return {
            c: ((r + i) % RANGE) for (i, c) in enumerate(labels)
        }
    fill = [_row(r) for r in range(nrow)]
    return DfRow(fill)


FILTER = 2


def time_filter(df):
    def f(label_0, **args):
        return label_0 % FILTER == 1
    start = time.time()
    df.filter(f)
    return time.time() - start

SELECT = 3

def time_select(df):
    indices = [i for i in range(df.ncol()) if ((i % SELECT) == 0)]
    labels = [f"label_{i}" for i in indices]
    start = time.time()
    df.select(*labels)
    return time.time() - start


def sweep(sizes):
    result = []
    for (nrow, ncol) in sizes:
        df_col = make_col(nrow, ncol)
        df_row = make_row(nrow, ncol)
        times = [
            time_filter(df_col),
            time_select(df_col),
            time_filter(df_row),
            time_select(df_row),
        ]
        result.append([nrow, ncol, *times])
    return result


def test():
    sizes = [(10, 10), (50, 50), (100, 100), (500, 500), (1000, 1000)]
    result = sweep(sizes)
    from pprint import pprint
    pprint(result)


if __name__ == '__main__':
    test()
    
