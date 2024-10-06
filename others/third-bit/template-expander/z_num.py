def open(expander, node):
    expander.show_tag(node)
    expander.output(node.attrs["z-num"])


def close(expander, node):
    expander.show_tag(node, closing=True)
