for i in nuke.selectedNodes():
    f1 = i.knob('from1').getValue()
    f2 = i.knob('from2').getValue()
    f3 = i.knob('from3').getValue()
    f4 = i.knob('from4').getValue()
    
    i.knob('from1').setAnimated()
    i.knob('from1').setValue(f1)
    i.knob('from2').setAnimated()
    i.knob('from2').setValue(f2)
    i.knob('from3').setAnimated()
    i.knob('from3').setValue(f3)
    i.knob('from4').setAnimated()
    i.knob('from4').setValue(f4)
