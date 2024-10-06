def open(expander, node):
    index_name, target = node.attrs["z-loop"].split(":")
    target = expander.env.find(target)
    expander.show_tag(node)
    for item in target:
        expander.env.push({index_name: item})
        for child in node.children:
            expander.walk(child)
        expander.env.pop()
    return False

def close(expander, node):
    expander.show_tag(node, closing=True)
        
