for i in nuke.selectedNodes():
    i.knob('knobChanged').setValue('n = nuke.thisNode()\nk = nuke.thisKnob()\nif k.name() == "which":\n    mult = n["which"].value()\n    r = int(200 * mult) + 40\n    g = int(200 * mult) + 40\n    b = int(200 * mult) + 40\n    hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)\n    n.knob("tile_color").setValue(int(hexColor))')
    i['label'].setValue('Which: [value which]')
    i.setSelected(False)
