# Fibonacci sequence: https://www.mathsisfun.com/numbers/fibonacci-sequence.html


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n > 1:
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


if __name__ == "__main__":

    print("fib recursive")
    for i in range(11):
        print(fib(i))

    print("fib iterative")
    for i in range(11):
        print(fib_iterative(i))

    print("fib iterative 2")
    for i in range(11):
        print(fib_iterative2(i))
