import nuke


nodes_before_selection = nuke.allNodes()

sel = nuke.selectedNodes()
for node in sel:
    node.selectOnly()
    nuke.nodePaste('%clipboard%')
    
[n.setSelected(True) for n in nuke.allNodes() if n not in nodes_before_selection]
