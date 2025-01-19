import sys
from architecture import *


OPS_LOOKUP = {value["code"]: key for key, value in OPS.items()}

class VirtualMachine:

    def __init__(self, writer=sys.stdout, reader=input):
        self.writer = writer
        self.reader = reader
        self.initialize([])
        self.prompt = ">>"

    def initialize(self, program):
        assert len(program) <= RAM_LEN, "Program too long"
        self.ram = [
            program[i] if i < len(program) else 0
            for i in range(RAM_LEN)
        ]
        self.ip = 0
        self.reg = [0] * NUM_REG

    def fetch(self):
        instruction = self.ram[self.ip]
        self.ip += 1
        op = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg0 = instruction & OP_MASK
        instruction >>= OP_SHIFT
        arg1 = instruction & OP_MASK
        return [op, arg0, arg1]

    def run(self):
        self.state = VMState.STEPPING
        while True:
            if self.state == VMState.STEPPING:
                self.interact(self.ip)
            if self.state == VMState.FINISHED:
                break
            instruction = self.ram[self.ip]
            self.ip += 1
            op, arg0, arg1 = self.decode(instruction)
            self.execute(op, arg0, arg1)

    def disassemble(self, addr, instruction):
        op, arg0, arg1 = self.decode(instruction)
        assert op in OPS_LOOKUP, f"Unknown op code {op} at {addr}"
        return f"{OPS_LOOKUP[op]} | {arg0} | {arg1}"

    def write(self, *args):
        line = "".join(args) + "\n"
        self.writer.write(line)

    def read(self, prompt):
        return self.reader(prompt).strip()    


class Assembler:

    DIVIDER = ".data"

    def assemble(self, lines):
        lines = self._get_lines(lines)
        to_compile, to_allocate = self._split(lines)

        labels = self._find_labels(lines)
        instructions = [
            line for line in to_compile if not self._is_label(line)
        ]

        base_of_data = len(instructions)
        self._add_allocations(base_of_data, labels, to_allocate)

        compiled = [
            self._compile(inst, labels) for inst in instructions
        ]
        program = self._to_text(compiled)
        return program

    def _add_allocations(self, base_of_data, labels, to_allocate):
        for allocation in to_allocate:
            fields = [a.strip() for a in allocation.split(':')]
            assert len(fields) == 2, "Invalid directive"
            label, num_words = fields
            assert label not in labels, f"Duplicate label in allocations: {label}"
            num_words = int(num_words)
            assert (base_of_data + num_words) < RAM_LEN, f"Allocation {label} exceeds available memory"
            labels[label] = base_of_data
            base_of_data += num_words

    def _split(self, lines):
        try:
            split = lines.index(self.DIVIDER)
            return lines[0:split], lines[split+1:]
        except ValueError:
            return lines, []

    def _find_labels(self, lines):
        result = {}
        loc = 0
        for l in lines:
            if self._is_label(l):
                label = l[:-1].strip()
                assert label not in result, f"Duplicated label: {label}"
                result[label] = loc
            else:
                loc += 1
        return result

    def _is_label(self, line):
        return line.endswith(":")

    def _compile(self, instruction, labels):
        tokens = instruction.split()
        op, args = tokens[0], tokens[1:]
        fmt, code = OPS[op]['fmt'], OPS[op]['code']

        if fmt == "--":
            return self._combine(code)
        elif fmt == "r-":
            return self._combine(self._reg(args[0]), code)
        elif fmt == "rr":
            return self._combine(self._reg(args[1]), self._reg(args[0]), code)
        elif fmt == "rv":
            return self._combine(self._val(args[1], labels), self._reg(args[0]), code)

    def _val(self, token, labels):
        if not token.startswith("@"):
            return int(token)
        label = token[1:]
        assert label in labels, f"Unknown label: {label}"
        return labels[label]

    def _reg(self, token):
        assert token.startswith('R'), f"Incorrect register: {token}"
        register_number = int(token[1:])
        assert 0 <= register_number < NUM_REG, f"Missing register: {token}"
        return register_number

    def _combine(self, *args):
        assert len(args) > 0
        result = 0
        for a in args:
            result <<= OP_SHIFT
            result |= a
        return result

    def _get_lines(self, raw_lines):
        return [l for l in raw_lines if not l.startswith('#') and len(l.strip())]

    def _to_text(self, instructions):
        return [hex(i) for i in instructions]

class Writer:
    def __init__(self):
        self.seen = []

    def write(self, *args):
        self.seen.extend(args)


class Reader:
    def __init__(self, *args):
        self.commands = args
        self.index = 0

    def __call__(self, prompt):
        assert self.index < len(self.commands)
        self.index += 1
        return self.commands[self.index - 1]


def execute(source, reader, writer):
    program = Assembler().assemble(source.split("\n"), False)
    vm = VirtualMachine(writer, reader)
    vm.initialize(program)
    vm.run()


def test_disassemble():
    source = """
    hlt
    """
    reader = Reader("d", "q")
    writer = Writer()
    execute(source, reader, writer)
    assert writer.seen == ["hlt | 0 | 0\n"]

def test_print_two_values():
    source = """
    ldc R0 55
    prr R0
    ldc R0 65
    prr R0
    hlt
    """
    reader = Reader("s", "s", "s", "q")
    writer = Writer()
    execute(source, reader, writer)
    assert writer.seen == [
        "000037\n"
    ]


def main():
    lines = [l.strip() for l in sys.stdin]
    print(f"Original: {lines}")
    assembled = Assembler().assemble(lines)
    print(f"Assembled: {assembled}")

    vm = VirtualMachine()
    vm.initialize([int(instruction, base=16) for instruction in assembled])
    vm.run()
    

if __name__ == '__main__':
    main()
