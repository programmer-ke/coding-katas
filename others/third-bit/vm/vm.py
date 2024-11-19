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
