import sys
from architecture import *


class VirtualMachine:

    def __init__(self):
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
        running = True
        while running:
            op, arg0, arg1 = self.fetch()
            if op == OPS['hlt']['code']:
                running = False
            elif op == OPS['ldc']['code']:
                self.reg[arg0] = arg1
            elif op == OPS['ldr']['code']:
                self.reg[arg0] = self.ram[self.reg[arg1]]
            elif op == OPS['cpy']['code']:
                self.reg[arg0] = self.reg[arg1]
            elif op == OPS['str']['code']:
                self.ram[self.reg[arg1]] = self.reg[arg0]
            elif op == OPS['add']['code']:
                self.reg[arg0] += self.reg[arg1]
            elif op == OPS['sub']['code']:
                self.reg[arg0] -= self.reg[arg1]
            elif op == OPS['beq']['code']:
                if self.reg[arg0] == 0:
                    self.ip = arg1
            elif op == OPS['bne']['code']:
                if self.reg[arg0] != 0:
                    self.ip = arg1
            elif op == OPS['prr']['code']:
                print(self.reg[arg0])
            elif op == OPS['prm']['code']:
                print(self.ram[self.reg[arg0]])
            else:
                assert False, f"Unknown op {op:06x}"


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
