import nuke


def get_top_node(nodes):
    temp_dict = {}
    for node in nodes:
        temp_dict[node] = node.ypos()
    temp_dict = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])}
    l = [k for k in temp_dict]
    return l[0]
        

selected = nuke.selectedNodes()

top_node = get_top_node(selected)

for node in [node for node in selected if node != top_node]:
    node.setInput(0, top_node)
