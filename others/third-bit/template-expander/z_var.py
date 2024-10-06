def open(expander, node):
    expander.show_tag(node)
    expander.output(expander.env.find(node.attrs["z-var"]))


def close(expander, node):
    expander.show_tag(node, closing=True)
