import nuke
import nukescripts

            
def try_to_set_knob_values(from_node, to_node):
    for k_name in from_node.knobs():
        try:
            if not k_name == "name":
                to_node[k_name].setValue(from_node[k_name].value())
        except:
            pass

for node in [n for n in nuke.selectedNodes()]:
    
    x, y = node.xpos(), node.ypos()
    
    TASK = nuke.ProgressTask("Creating rotos...")
    TASK.setMessage("Please, wait...")
    
    counter = 0
    for shape in node["curves"].rootLayer:
        
        if TASK.isCancelled():
            break
        
        x = x + 125
        
        new_node = nuke.nodes.Roto()
        try_to_set_knob_values(from_node=node, to_node=new_node)
        
        new_node['curves'].rootLayer.setTransform(node['curves'].rootLayer.getTransform())
        
        new_node.setXYpos(x, y)
        
        new_node.setName(node.name() + "_" + shape.name)
        
        new_node['curves'].rootLayer.append(shape.clone())
        
        TASK.setProgress(int(float(counter) / float(len(node["curves"].rootLayer)) * 100))
        counter += 1
    
    node.setSelected(False)
    
    TASK.setProgress(100)
    del TASK
