import nuke
import nukescripts


class Panel(nukescripts.PythonPanel):
    def __init__(self, nodes):
        nukescripts.PythonPanel.__init__(self, 'Set Value For Knobs')
        
        self.nodes = nodes
        self.setupUI()
        
    def setupUI(self):
        self.p_knobs = nuke.Enumeration_Knob("p_knobs", "Knob:", sorted([k.name() for k in self.nodes[0].allKnobs()]))
        self.addKnob(self.p_knobs)
        
        self.p_value = nuke.String_Knob("p_value", "Value:")
        self.addKnob(self.p_value)
        
        self.p_button = nuke.PyScript_Knob("p_button", "Set!")
        self.addKnob(self.p_button)
        self.p_button.setFlag(nuke.STARTLINE)

    def knobChanged(self, knob):
        if knob == self.p_button:
            self.set()
        
    def set(self):
        try:
            for node in self.nodes:
                node[self.p_knobs.value()].setValue(self.p_value.value())
            if not nuke.ask("Done! Do you want to continue?"):
                self.destroy()
        except:
            nuke.message("Error! Try again.")

nodes = []
for node in nuke.selectedNodes():
    nodes.append(node)
    
# nodes_have_one_class = True
# for node in nodes:
    # if node.Class() != nodes[0].Class():
        # nodes_have_one_class = False

if True:
    p = Panel(nodes)
    p.showModal()
else:
    nuke.message("Please select same Class nodes!")
