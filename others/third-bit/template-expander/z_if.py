def open(expander, node):
    flag = expander.env.find(node.attrs["z-if"])
    if flag:
        expander.show_tag(node)
    return flag


def close(expander, node):
    flag = expander.env.find(node.attrs["z-if"])
    if flag:
        expander.show_tag(node, closing=True)
    
