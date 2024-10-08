import ast
import sys
from collections import defaultdict


class CollectNames(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.names = defaultdict(set)

    def visit_Assign(self, node):
        for var in node.targets:
            self.add(var, var.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.add(node, node.name)
        self.generic_visit(node)

    def add(self, node, name):
        loc = (node.lineno, node.col_offset)
        self.names[name].add(loc)

    def position(self, node):
        return ({node.lineno}, {node.col_offset})
            

def main():
    with open(sys.argv[1], 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    collector = CollectNames()
    collector.visit(tree)
    print(collector.names)


if __name__ == '__main__':
    main()
