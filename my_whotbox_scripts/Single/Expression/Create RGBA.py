def set_channel(node, channel):
    count = 0
    while count < 4:
        node.knob('expr' + str(count)).setValue(channel)
        count += 1

for i in nuke.selectedNodes():
    exprR = nuke.nodes.Expression(name='R')
    exprG = nuke.nodes.Expression(name='G')
    exprB = nuke.nodes.Expression(name='B')
    exprA =  nuke.nodes.Expression(name='A')
    dot = nuke.nodes.Dot()
    
    set_channel(exprR, 'r')
    set_channel(exprG, 'g')
    set_channel(exprB, 'b')
    set_channel(exprA, 'a')
    
    exprR.setXpos(i.xpos() - 150)
    exprR.setYpos(i.ypos())
    exprG.setXpos(i.xpos())
    exprG.setYpos(i.ypos())
    exprB.setXpos(i.xpos() + 150)
    exprB.setYpos(i.ypos())
    exprA.setXpos(i.xpos() + 300)
    exprA.setYpos(i.ypos())
    dot.setXpos(i.xpos() + 108)
    dot.setYpos(i.ypos() - 100)
    
    # blood color
    r = int(141)
    g = int(81)
    b = int(93)
    hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)
    exprR.knob("tile_color").setValue(int(hexColor))
    
    # grass color
    r = int(105)
    g = int(139)
    b = int(114)
    hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)
    exprG.knob("tile_color").setValue(int(hexColor))
    
    # ocean color
    r = int(66)
    g = int(97)
    b = int(109)
    hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)
    exprB.knob("tile_color").setValue(int(hexColor))
    
    exprR.setInput(0, dot)
    exprG.setInput(0, dot)
    exprB.setInput(0, dot)
    exprA.setInput(0, dot)
    
    nuke.delete(i)
