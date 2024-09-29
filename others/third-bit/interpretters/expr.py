import json
import sys


def do_add(env, args):
    assert len(args) == 2
    left = do(env, args[0])
    right = do(env, args[1])
    return left + right


def do_abs(env, args):
    assert len(args) == 1
    value = do(env, args[0])
    return abs(value)


def do(env, expr):

    if isinstance(expr, int):
        return expr
    elif isinstance(expr, list) and (op := expr[0]) in OPS:
        return OPS[op](env, expr[1:])
    else:
        raise ValueError(f"Unknown expression: {expr}")


def do_get(env, args):
    match args:
        case [str(var_name)]:
            return env[var_name]
        case _:
            raise ValueError(f"Unknown variable: {args}")


def do_set(env, args):
    match args:
        case [str(var_name), expr]:
            value = do(env, expr)
            env[var_name] = value
            return value
        case _:
            raise ValueError(f"Unknown variable name and value: {args}")


def do_seq(env, args):
    assert len(args) > 0
    for expr in args:
        result = do(env, expr)
    return result


OPS = {
    name.replace("do_", ""): op
    for name, op in globals().items()
    if name.startswith("do_")
}


def main():
    if not len(sys.argv) == 2:
        print("Usage: expr.py filename")
        sys.exit(1)
    with open(sys.argv[1], 'r') as f:
        program = json.load(f)

    env = {}
    result = do(env, program)
    print(f"=> {result}")


if __name__ == "__main__":
    main()
