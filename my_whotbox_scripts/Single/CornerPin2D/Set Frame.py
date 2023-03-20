frame = str(nuke.frame())

for i in nuke.selectedNodes():
    i.knob('copy_to').execute()
    i.knob('from1').clearAnimated()
    i.knob('from2').clearAnimated()
    i.knob('from3').clearAnimated()
    i.knob('from4').clearAnimated()
