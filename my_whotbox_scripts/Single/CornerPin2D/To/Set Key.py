for i in nuke.selectedNodes():
    f1 = i.knob('to1').getValue()
    f2 = i.knob('to2').getValue()
    f3 = i.knob('to3').getValue()
    f4 = i.knob('to4').getValue()
    
    i.knob('to1').setAnimated()
    i.knob('to1').setValue(f1)
    i.knob('to2').setAnimated()
    i.knob('to2').setValue(f2)
    i.knob('to3').setAnimated()
    i.knob('to3').setValue(f3)
    i.knob('to4').setAnimated()
    i.knob('to4').setValue(f4)
