# Add selected nodes to dictionary for sort in by position
dict_trackers = {}
for i in nuke.selectedNodes():
    Y = i.ypos()
    dict_trackers[Y] = i
list_dict_trackers = sorted(dict_trackers.items())

# Select all nodes
for i in nuke.allNodes():
    i.setSelected(True)
    
# Create new nodes
for key, value in list_dict_trackers:
    value.knob("cornerPinOptions").setValue(5)
    value.knob("createCornerPin").execute()
    
# Inverst selection to select new created nodes
nuke.invertSelection()


# Get list of new created nodes
list_new_trackers = []
for I in nuke.selectedNodes():
    list_new_trackers.append(I)

# Connect bot new nodes to top new nodes
lenth = len(list_new_trackers)
if lenth > 1:
    bot = 0
    top = 1
    while bot != lenth-1:
        list_new_trackers[bot].setInput(0, list_new_trackers[top])
        bot = bot + 1
        top = top + 1
