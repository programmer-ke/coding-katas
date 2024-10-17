class SaveObjects:
    def __init__(self, writer):
        self.writer = writer

    def save(self, thing):
        type_name = type(thing).__name__
        method_name = f"save_{type_name}"
        assert hasattr(self, method_name), f"Unknown object type {method}"
        method = getattr(self, method_name)
        method(thing)

    def save_int(self, thing):
        self._write('int', thing)

    def save_str(self, thing):
        lines = thing.split('\n')
        self.write('str', len(lines))
        for line in lines:
            print(line, file=self.writer)

    def _write(self, left, right):
        print(f'{left}:{right}', file=self.writer)


class LoadObjects:
    def __init__(self, reader):
        self.reader = reader

    def load(self):
        line = self.reader.readline()[:-1]
        assert line, "nothing to read"
        fields = line.split(":", maxsplit=1)
        assert len(fields) == 2, f"Badly formed line: {line}"
        key, value = fields
        method_name = f"load_{key}"
        assert hasattr(self, method_name), f"Unknown object type: {key}"
        return getattr(self, method_name)(value)

    def load_float(self, value):
        return float(value)
