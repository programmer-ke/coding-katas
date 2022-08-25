# Fibonacci sequence:
# https://www.mathsisfun.com/numbers/fibonacci-sequence.html


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n > 1:
        # note the repeated computations
        return fib(n - 1) + fib(n - 2)


def fib_iterative(n):
    if n == 0:
        num = 0
    elif n == 1:
        num = 1
    else:
        n_1, n_2 = 1, 0
        for i in range(2, n + 1):
            num = n_1 + n_2
            n_1, n_2 = num, n_1
    return num


def fib_iterative2(n):
    if n == 0:
        num = 0
    elif n == 1:
        num = 1
    else:
        n_1, n_2 = 1, 0
        i = 2
        while i <= n:
            num = n_1 + n_2
            n_1, n_2 = num, n_1
            i += 1
    return num

def fib_iterative3(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    i = 1
    a, b = 0, 1
    while True:
        # re-assigns the next out of use variable
        i += 1
        a = a + b
        if i == n:
            return a
        i += 1
        b = a + b
        if i == n:
            return b


if __name__ == "__main__":

    # recursive
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    recursive = [fib(i) for i in range(11)]
    assert expected == recursive

    # iterative
    iterative = [fib_iterative(i) for i in range(11)]
    assert expected == iterative

    # iterative 2
    iterative_2 = [fib_iterative2(i) for i in range(11)]
    assert expected == iterative_2

    # iterative 3
    iterative_3 = [fib_iterative3(i) for i in range(11)]
    assert expected == iterative_3
