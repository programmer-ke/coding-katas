from bs4 import BeautifulSoup, NavigableString, Tag

def display(node):
    if isinstance(node, NavigableString):
        print(f"string: {repr(node.string)}")
        return
    else:
        print(f"node: {node.name}")
        for child in node:
            display(child)


text = """<html>
<body>
<h1>Title</h1>
<p>paragraph</p>
</body>
</html>"""

doc = BeautifulSoup(text, "html.parser")
display(doc)


def display(node):
    if isinstance(node, Tag):
        print(f"node: {node.name} {node.attrs}")
        for child in node:
            display(child)


text = """<html lang="en">
<body class="outline narrow">
<p align="left" align="right">paragraph</p>
</body>
</html>"""

doc = BeautifulSoup(text, "html.parser")
display(doc)
