import ast


nuke_ver = nuke.NUKE_VERSION_MAJOR


if nuke_ver >= 13:
    def maxValue(srcNode, channel='red'):
        expr = nuke.nodes.Expression(inputs=[srcNode], expr0="a")
        grade = nuke.nodes.Grade(inputs=[expr], channels=channel, white=100)
        reformat = nuke.nodes.Reformat(inputs=[grade], type=2, scale=0.1, filter=0)
        width = reformat.width()
        height = reformat.height()
        curve_tool = nuke.nodes.CurveTool(inputs=[reformat], channels=channel)
        curve_tool.knob('ROI').setValue(width, 2)
        curve_tool.knob('ROI').setValue(height, 3)
        nuke.execute(curve_tool, nuke.frame(), nuke.frame())
        maxValue = curve_tool.knob('intensitydata').value()
        
        nuke.delete(grade)
        nuke.delete(reformat)
        nuke.delete(curve_tool)
        nuke.delete(expr)
        
        return maxValue
    
    
    for crypt in nuke.selectedNodes():
        
        # create matte_list
        metadate = crypt.metadata()
        for key in metadate:
            if 'manifest' in key:
                metadate_values = metadate[key]
        
        matte_list = []
        for key in ast.literal_eval(metadate_values):
            matte_list.append(key)
           
         
        # delete cryptomatte node, find read node
        read = (crypt.dependencies())[0]
        nuke.delete(crypt)
        
        count = 0
        count_x = 0
        while count < len(matte_list):
            color_green = 16712451
            dot = nuke.nodes.Dot(inputs=[read], hide_input=1, tile_color=color_green)
            crypt_new = nuke.nodes.Cryptomatte(inputs=[dot], matteList=matte_list[count])
            
            if maxValue(crypt_new) == 0:
                nuke.delete(crypt_new)
                nuke.delete(dot)
            else:
                expr = nuke.nodes.Expression(inputs=[crypt_new], expr0="a*10", expr1="a*10", expr2="b+a*10", postage_stamp=True, tile_color=color_green)
                
                crypt_new.setXpos(read.xpos() + count_x)
                dot.setXpos(read.xpos() + count_x + 34)
                expr.setXpos(read.xpos() + count_x)
                
                crypt_new.setYpos(read.ypos() + 150)
                dot.setYpos(read.ypos() + 120)
                expr.setYpos(crypt_new.ypos() + 25)
                
                count_x += 100
                
            count += 1
            
            
elif nuke_ver == 12:
    # Function to understand if channel red is zero or not
    def getMax(srcNode, channel='red'):
        grade = nuke.nodes.Grade(inputs=[srcNode], channels=channel, white=100)
        reformat = nuke.nodes.Reformat(inputs=[grade], type=2, scale=0.1, filter=0)
        width = reformat.width()
        height = reformat.height()
        curve_tool = nuke.nodes.CurveTool(inputs=[reformat], channels=channel)
        curve_tool.knob('ROI').setValue(width, 2)
        curve_tool.knob('ROI').setValue(height, 3)
        nuke.execute(curve_tool, nuke.frame(), nuke.frame())
        maxValue = curve_tool.knob('intensitydata').value()
        
        nuke.delete(grade)
        nuke.delete(reformat)
        nuke.delete(curve_tool)
        
        return maxValue
        

    # Bake all selected cryptomatte nodes
    cryptomattes = []
    for i in nuke.selectedNodes():
        cryptomattes.append(i)
        i.setSelected(False)
    
    # Main
    for cryptomatte in cryptomattes:
        
        # Select all projects nodes
        nodes_selected_old = []
        for i in nuke.allNodes():
            nodes_selected_old.append(i.name())
        
        # Execute manifest from cryptomatte
        cryptomatte.knob('unloadManifest').execute()
        
        
        # Take read name and delete cryptomatte node
        read = (cryptomatte.dependencies())[0]
        nuke.delete(cryptomatte)
        
        # Select new created nodes
        nodes_selected_new = []
        for i in nuke.allNodes():
            if not i.name() in nodes_selected_old:
                nodes_selected_new.append(i)
        
        
        for i in nodes_selected_new:
            #delete empty nodes
            maxV = getMax(i)
            if maxV == 0:
                nuke.delete(i)
    
            # select not empty nodes
            if i in nuke.allNodes():
                i.setSelected(True)
        
        # not empty nodes: postion, organize
        count_nodes = 0
        count_postion = 0
        while count_nodes <= len(nuke.selectedNodes()):
            for i in nuke.selectedNodes():
                i.knob('postage_stamp').setValue(True)
                i.setYpos(read.ypos()+225)
                i.setXpos(read.xpos() + count_postion)
                
                dot = nuke.nodes.Dot(hide_input=1, tile_color=16712451)
                dot.setXpos(i.xpos()+33)
                dot.setYpos(i.ypos()-50)
                dot.setInput(0, read)
                i.setInput(0, dot)
                dot.knob('hide_input').setValue(1)
                dot.knob('hide_input').setValue(1)
                
                count_nodes += 1
                count_postion += 125
                
                i.setSelected(False)
                
    
    # add choice for details (decrease or increase scale in reformat)
    # arrange in node graph nodes
    # make good text for all knobs
    # make beautiful connections to all knobs
elif nuke_ver < 12:
    nuke.message('Version of nuke is not supported. Sorryy...')
