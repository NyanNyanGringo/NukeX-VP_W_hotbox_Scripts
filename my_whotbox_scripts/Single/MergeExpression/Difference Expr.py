for i in nuke.selectedNodes():
    i.knob('expr0').setValue('0')
    i.knob('expr1').setValue('0')
    i.knob('expr2').setValue('0')
    i.knob('expr3').setValue('Ar!=Br||Ag!=Bg||Ab!=Bb ? 1 : 0')
    
    i['label'].setValue('a: [value expr3]')
