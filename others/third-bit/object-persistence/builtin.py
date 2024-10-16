from textwrap import dedent
from io import StringIO
import sys


def save(writer, thing):

    if isinstance(thing, str):
        lines = thing.split("\n")
        print(f"str:{len(lines)}", file=writer)
        for line in lines:
            print(line, file=writer)
    
    elif isinstance(thing, bool):
        print(f"bool:{thing}", file=writer)

    elif isinstance(thing, float):
        print(f"float:{thing}", file=writer)

    elif isinstance(thing, int):
        print(f"int:{thing}", file=writer)

    elif isinstance(thing, list):
        print(f"list:{len(thing)}", file=writer)
        for item in thing:
            save(writer, item)

    elif isinstance(thing, set):
        print(f"set:{len(thing)}", file=writer)
        for item in thing:
            save(writer, item)

    elif isinstance(thing, dict):
        print(f"dict:{len(thing)}", file=writer)
        for key, value in thing.items():
            save(writer, key)
            save(writer, value)

    else:
        raise ValueError(f"Unknown thing: {thing} of type: {type(thing)}")


def load(reader):
    line = reader.readline()[:-1]
    assert line, "nothing to read"
    fields = line.split(":", maxsplit=1)
    assert len(fields) == 2, f"Badly-formed line: {line}"
    key, value = fields

    if key == 'bool':
        names = {"True": True, "False": False}
        assert value in names, f"Unknown boolean: {value}"
        return names[value]

    elif key == "float":
        return float(value)

    elif key == "int":
        return int(value)

    elif key == "str":
        return  "\n".join([reader.readline()[:-1] for _ in range(int(value))])

    elif key == "list":
        return [load(reader) for _ in range(int(value))]

    elif key == "set":
        return {load(reader) for _ in range(int(value))}

    elif key == "dict":
        return {load(reader): load(reader) for _ in range(int(value))}

    else:
        raise ValueError(f"Unknown thing {line}")

def test_save_list_flat():
    fixture = [0, False]
    expected = dedent("""\
    list:2
    int:0
    bool:False
    """)
    output = StringIO()
    save(output, fixture)
    assert output.getvalue() == expected


def test():
    for k, obj in globals().items():
        if k.startswith("test_"):
            obj()


def main():
    test()
    save(sys.stdout, [False, 3.14, "hello", {"left": 1, "right": [2, 3]}])


if __name__ == '__main__':
    main()
