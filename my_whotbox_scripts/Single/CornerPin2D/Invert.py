for i in nuke.selectedNodes():
    inv = i.knob('invert').value()
    i.knob('invert').setValue(1-inv)
