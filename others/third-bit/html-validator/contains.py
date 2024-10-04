import sys
from bs4 import BeautifulSoup, NavigableString, Tag


def recurse(node, catalog):
    
    if node.name not in catalog:
        catalog[node.name] = set()

    for child in node:
        if isinstance(child, Tag):
            catalog[node.name].add(child.name)
            recurse(child, catalog)

    return catalog


if __name__ == "__main__":
    assert len(sys.argv) == 2
    with open(sys.argv[1]) as f:
        text = f.read()
    doc = BeautifulSoup(text, 'html.parser')
    catalog = recurse(doc, {})
    for k, v in catalog.items():
        print(k, v)
