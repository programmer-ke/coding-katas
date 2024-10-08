import ast
import sys
from collections import Counter


class FindDuplicateKeys(ast.NodeVisitor):
    def visit_Dict(self, node):
        seen = Counter()
        for key in node.keys:
            if isinstance(key, ast.Constant):
                seen[key.value] += 1
        problems = {k for k, v in seen.items() if v > 1}
        self.report(node, problems)
        self.generic_visit(node)

    def report(self, node, problems):
        if problems:
            msg = ", ".join(p for p in problems)
            print(f"duplicate key(s) {{{msg}}} at {node.lineno}")
    
            
def main():
    with open(sys.argv[1], 'r') as f:
        source = f.read()

    tree = ast.parse(source)
    checker = FindDuplicateKeys()
    checker.visit(tree)


if __name__ == '__main__':
    main()
