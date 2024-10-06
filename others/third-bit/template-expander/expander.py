import json
import sys

from bs4 import BeautifulSoup, NavigableString

import z_var
import z_num
import z_if
import z_loop


HANDLERS = {
    "z-var": z_var,
    "z-num": z_num,
    "z-if": z_if,
    "z-loop": z_loop, 
}


class Env:

    def __init__(self, initial):
        self.stack = [initial.copy()]

    def push(self, frame):
        self.stack.append(frame.copy())

    def pop(self):
        return self.stack.pop()

    def find(self, name):
        for frame in reversed(self.stack):
            if name in frame:
                return frame[name]
        return None


class Visitor:
    def __init__(self, root):
        self.root = root

    def walk(self, node=None):
        if node is None:
            node = self.root

        if self.open(node):

            for child in node.children:
                self.walk(child)

        self.close(node)

    def open(self, node):
        raise NotImplementedError("open")

    def close(self, node):
        raise NotImplementedError("close")


class Expander(Visitor):

    def __init__(self, root, variables):
        super().__init__(root)
        self.env = Env(variables)
        self.handlers = HANDLERS
        self.result = []

    def open(self, node):
        if isinstance(node, NavigableString):
            self.output(node.string)
            return False
        elif handler := self.get_handler(node):
            return handler.open(self, node)
        else:
            self.show_tag(node)
            return True

    def close(self, node):
        if isinstance(node, NavigableString):
            return
        elif handler := self.get_handler(node):
            handler.close(self, node)
        else:
            self.show_tag(node, closing=True)

    def get_handler(self, node):
        possible = [name for name in node.attrs if name in self.handlers]
        return self.handlers[possible[-1]] if possible else None
    
    def show_tag(self, node, closing=False):
        if closing:
            self.output(f"</{node.name}>")
        else:
            self.output(f"<{node.name}")
            for attr, value in node.attrs.items():
                if not attr.startswith("z-"):
                    self.output(f" {attr}={value}")
            self.output(">")

    def output(self, text):
        self.result.append("UNDEF" if text is None else text)

    def get_result(self):
        return "".join(self.result)



def main():
    with open(sys.argv[1]) as f:
        variables = json.load(f)

    with open(sys.argv[2]) as f:
        doc = BeautifulSoup(f.read(), "html.parser")
        template = doc.find("html")

    expander = Expander(template, variables)
    expander.walk()
    print(expander.get_result())


if __name__ == '__main__':
    main()
