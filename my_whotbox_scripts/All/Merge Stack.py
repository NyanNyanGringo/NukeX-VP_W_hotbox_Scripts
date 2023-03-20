# get next node down tree (if node has multiple outputs, get first one found)
def getOutNode(n):

    # this sometimes fails on first try, just do it again
    listDotOut = n.dependent()
    dotOut = None

    # go through dependent nodes and see if they are connected with hidden pipes or if they are viewers
    for outNode in listDotOut:

        #if not, make this the node to make a corner with
        if (not outNode.Class() == "Viewer") and (not outNode['hide_input'].getValue()):

            dotOut = outNode
            break



    # return single node
    return dotOut




def PlaceInCorner(dotsToAlign, forceXpos=-.1):

    # get list of dots only
    dots = []

    # if all dots connect to same node, do not make corner dots
    SameDotOut = True if len(dotsToAlign) > 1 else False
    lastDotOut = None
    nodeClosestYPos = float("inf")
    multInputXPos = 0


    # for each selected node with 'Dot' as its class
    for n in dotsToAlign:

        if n.Class() == "Dot":

            # populate list
            dots.append(n)


            # only check if there's still a chance they're all the same
            if(SameDotOut):

                dotOut = getOutNode(n)

                if((dotOut == lastDotOut or lastDotOut == None) and not (dotOut == None) ):

                    # update store
                    lastDotOut = dotOut

                    # get the closest Ypos of input nodes to this output node
                    nodeClosestYPos = min( abs(dotOut.ypos() - n.input(0).ypos()), nodeClosestYPos )

                # found a difference
                else:

                    SameDotOut = False


    # go through all dots
    for dot in dots:

        # if knobs don't exist or something else is wrong, do not bother user
        try:

            # get the input and output nodes
            dotIn = dot.input(0)
            dotOut = getOutNode(dot)


            # get the input and output node position center (which is their position + half of their width and half of their height, as they are positioned by their corners)
            dotInX = dotIn.xpos() + (dotIn.screenWidth() // 2)
            dotInY = dotIn.ypos() + (dotIn.screenHeight() // 2)
            dotInP = [dotInX, dotInY]

            dotOutX = dotOut.xpos() + (dotOut.screenWidth() // 2)
            dotOutY = dotOut.ypos() + (dotOut.screenHeight() // 2)
            dotOutP = [dotOutX, dotOutY]

            # get the current dot position center
            dotX = dot.xpos() + (dot.screenWidth() // 2)
            dotY = dot.ypos() + (dot.screenHeight() // 2)
            dotP = [dotX, dotY]

            # determine where the dot should be
            goX = dotInX
            goY = dotOutY
            goP = [goX, goY]

            # check if the dot is already where it should be, and do also forceXpos check
            AlreadyThere = False
            if ((dotX == goX and dotY == goY) or (forceXpos != -.1 and forceXpos != goX)):
                AlreadyThere = True

            # if it is, or of the node is at the same position as its input or output node, do the following
            if (AlreadyThere or goP == dotInP or goP == dotOutP):

                # check if the dot is further away from the input than from the output node in X
                FarOut = False
                if (abs(dotX - dotInX) > abs(dotX - dotOutX)):
                    FarOut = True

                # check if the dot is further away from the input than from the output node in Y or if it is already where it should be
                if ((abs(dotY - dotInY) < abs(dotY - dotOutY)) or AlreadyThere):

                    # set the desired position to the output node X and the input node Y
                    goX = dotOutX
                    goY = dotInY

                    # but if that means the dot will be at the same position as it currently is, set it to the input node X and output node Y
                    if (dotX == goX and dotY == goY):
                        goX = dotInX
                        goY = dotOutY
                else:

                    if (FarOut or AlreadyThere):
                        goX = dotInX
                        goY = dotOutY


            # set dot position X
            dot.setXpos(goX - (dot.screenWidth() // 2))

            # set dot position Y
            if SameDotOut:
                dot.setYpos(lastDotOut.ypos() - nodeClosestYPos//3)
            else:
                dot.setYpos(goY - (dot.screenHeight() // 2))



        # on error, ignore
        except Exception as e:
            pass




# overall function that decides what needs to happen
def AlignDots(nodes = []):

    # list nodes to work with
    dotsToAlign = []
    if nodes == []:
        dotsToAlign = nuke.selectedNodes()
    else:
        dotsToAlign = nodes



    # force dots to be on same vertical line (for sidestreams), -.1 means ignore
    forceXpos = -.1



    # exceptions first: if there is one non-dot node selected, give all of its inputs dots
    if len(dotsToAlign) == 1:

        selNode = dotsToAlign[0]
        if not selNode.Class() == 'Dot':

            # make list of dots
            dots = []

            # temp list to go through first, then go to dots[] - for nodes that have multiple inputs but still only need 90-degree angles
            dotList = []



            # check if input and output are both connected to nodes in the same stream (to make dots on top and bottom of node)
            nIn = selNode.dependencies()
            nOut = selNode.dependent()
            sideStream = False

            if len(nIn) == 1 and len(nOut) == 1:
                if nIn[0].xpos() + nIn[0].screenWidth()//2 == nOut[0].xpos() + nOut[0].screenWidth()//2:
                    sideStream = True

            if sideStream:
                
                # make dots
                newDotIn = nuke.nodes.Dot()
                newDotOut = nuke.nodes.Dot()

                # connect
                newDotIn.setInput(0, nIn[0])
                selNode.setInput(0, newDotIn)

                newDotOut.setInput(0, selNode)

                # check which input of nOut is connected to this node
                for eachIn in range(nOut[0].inputs()):
                    if(nOut[0].input(eachIn) == selNode):
                        inputI = eachIn
                        nOut[0].setInput(eachIn, newDotOut)


                dots.append(newDotIn)
                dots.append(newDotOut)
                
                # select new dot
                newDotIn['selected'].setValue(True)
                newDotOut['selected'].setValue(True)

                forceXpos = selNode.xpos() + selNode.screenWidth()//2



            # if not a sidestream, do a per-input dot connect
            else:

                # get all of its inputs
                for inp in range(selNode.inputs()):

                    currInput = selNode.input(inp)

                    # only proceed if input is connected (for instance, Merge nodes can have A3 empty but A4 connected)
                    if currInput is not None:

                        # only proceed if node is not already at a 90-degree angle
                        if (currInput.ypos() + currInput.screenHeight()//2) != (dotsToAlign[0].ypos() + dotsToAlign[0].screenHeight()//2):

                            # add to temp list
                            dotList.append([inp, selNode.input(inp)])



                # check if only one dot can be put in 90-degree angle instead, for instance when merging with main stream
                if len(dotList) == 2:

                    first = False
                    second = False

                    # check first input
                    if (selNode.input(dotList[0][0]).xpos() + selNode.input(dotList[0][0]).screenWidth()//2) == (selNode.xpos() + selNode.screenWidth()//2):
                        first = True

                    if (selNode.input(dotList[1][0]).xpos() + selNode.input(dotList[1][0]).screenWidth()//2) == (selNode.xpos() + selNode.screenWidth()//2):
                        second = True


                    # only allow the second dot to be made
                    if first and not second:
                        dotList = [dotList[1]]

                    # only allow the first dot to be made
                    if second and not first:
                        dotList = [dotList[0]]
                        


                for newDots in dotList:

                    # make dot
                    newDot = nuke.nodes.Dot()

                    # connect
                    newDot.setInput(0, newDots[1])
                    selNode.setInput(newDots[0], newDot)

                    dots.append(newDot)
                    
                    # select new dot
                    newDot['selected'].setValue(True)




            # select new dot, deselect originally selected node
            selNode['selected'].setValue(False)

            # place all in corner
            PlaceInCorner(dots, forceXpos)
            


        # one node selected, but it's a dot
        else:
            PlaceInCorner(dotsToAlign)



    # if not, go through all selected nodes and place dots in corner
    else:
        PlaceInCorner(dotsToAlign)

def setNodePosition(toNode, aboutNode, pos='bot', dist=6, offset=[0, 0]):
    x1, y1 = toNode.xpos(), toNode.ypos()
    w1, h1 = toNode.screenWidth(), toNode.screenHeight()

    x2, y2 = aboutNode.xpos(), aboutNode.ypos()
    w2, h2 = aboutNode.screenWidth(), aboutNode.screenHeight()

    if pos == "bot":
        toNode.setXpos(x2 + w2//2 - w1//2 + offset[0])
        toNode.setYpos(y2 + h2 + dist + offset[1])
    elif pos == 'right':
        toNode.setXpos(x2 + w2 + dist + offset[0])
        toNode.setYpos(y2 + h2//2 - h1//2 + offset[1])
    elif pos == 'left':
        toNode.setXpos(x2 - w2 - dist + offset[0])
        toNode.setYpos(y2 + h2//2 - h1//2 + offset[1])
    elif pos == 'top':
        toNode.setXpos(x2 + w2//2 - w1//2 + offset[0])
        toNode.setYpos(y2 - h1 - dist + offset[1])
    elif pos == 'center':
        toNode.setXpos(x2 + w2//2 - w1//2 + offset[0])
        toNode.setYpos(y2 + h2//2 - h1//2 + offset[1])
    elif pos == 'default':
        toNode.setXpos(x2 + offset)
        toNode.setYpos(y2 + offset)
        
def get_list_of_nodes_in_right_order():
    temp_dict = {}
    for node in nuke.selectedNodes():
        temp_dict[node] = node.xpos()
    temp_dict = {k: v for k, v in sorted(temp_dict.items(), key=lambda item: item[1])}
    return [k for k in temp_dict]
    
def set_nodes_position(nodes):
    start_x = nodes[0].xpos()
    start_y = nodes[0].ypos()
    temp_x = start_x
    for node in nodes:
        if node == nodes[0]: continue
        node.setXpos(temp_x + 200)
        node.setYpos(start_y)
        temp_x += 200
        
def create_channel_merges(nodes):
    # reverse read list  
    final_read = nodes[::-1]
    
    # create ChannelMerges list
    cms = []
    # create Dots list
    dots = []
    # position var
    p = 200
    # counter for ChannelMerges
    i = 0
    # counter for Dots
    d = 0
    
    for n in range(0, len(final_read)-1):
        # Create ChannelMerge and Dot
        cm = nuke.nodes.Merge2()
        dot = nuke.nodes.Dot()
        
        # Set positions
        cm.setXYpos(final_read[0].xpos(), final_read[0].ypos() + p)
        setNodePosition(dot, final_read[d+1], 'bot')
        
        # Set inputs
        if len(cms) == 0:
            cm.setInput(0, final_read[0])
            cm.setInput(1, dot)
            dot.setInput(0, final_read[1])
        else:
            cm.setInput(0, cms[i])
            cm.setInput(1, dot)
            dot.setInput(0, final_read[i+2])
            i += 1
        
        # Append to list CM and Dot
        cms.append(cm)
        dots.append(dot)
        
        # Up
        p += 50
        d += 1
    
    for x in nuke.selectedNodes():
        x.setSelected(False)
        
    for d in dots:
        d.setSelected(True)
    AlignDots()
    
nodes = get_list_of_nodes_in_right_order()
set_nodes_position(nodes)
create_channel_merges(nodes)
