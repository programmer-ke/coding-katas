import sys
from bs4 import BeautifulSoup, NavigableString, Tag
import yaml


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


class Check(Visitor):
    def __init__(self, manifest):
        self.manifest = manifest
        self.problems = {}

    def _tag_enter(self, node):
        actual = {child.name for child in node if isinstance(child, Tag)}
        errors = actual - self.manifest.get(node.name, set())

        if errors:
            errors |= self.problems.get(node.name, set())
            self.problems[node.name] = errors


def read_manifest(filename):
    with open(filename, 'r') as f:
        result = yaml.load(f, Loader=yaml.FullLoader)
        for k in result:
            result[k] = set(result[k])
        return result


if __name__ == "__main__":

    assert len(sys.argv) == 3
    manifest = read_manifest(sys.argv[1])
    with open(sys.argv[2]) as f:
        text = f.read()
    doc = BeautifulSoup(text, 'html.parser')

    checker = Check(manifest)
    checker.visit(doc.html)
    for tag, contents in sorted(checker.problems.items()):
        print(f"{tag}: {', '.join(sorted(contents))}")
