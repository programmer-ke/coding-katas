import sys
from bs4 import BeautifulSoup, NavigableString, Tag


class Visitor:
    def visit(self, node):
        if isinstance(node, NavigableString):
            self._text(node)
        if isinstance(node, Tag):
            self._tag_enter(node)
            for child in node:
                self.visit(child)
            self._tag_exit(node)

    def _text(self, node): pass
    def _tag_enter(self, node): pass
    def _tag_exit(self, node): pass


class Catalog(Visitor):

    def __init__(self):
        super().__init__()
        self.catalog = {}

    def _tag_enter(self, node):
        if node.name not in self.catalog:
            self.catalog[node.name] = set()
        for child in node:
            if isinstance(child, Tag):
                self.catalog[node.name].add(child.name)

if __name__ == "__main__":
    assert len(sys.argv) == 2
    with open(sys.argv[1]) as f:
        text = f.read()
    doc = BeautifulSoup(text, 'html.parser')
    cataloger = Catalog()
    cataloger.visit(doc.html)
    for tag, contents in sorted(cataloger.catalog.items()):
        print(f"{tag}: {', '.join(sorted(contents))}")

    
