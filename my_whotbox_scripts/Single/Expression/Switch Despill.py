for i in nuke.selectedNodes():
    blue = 'b>(r+g)/2?(r+g)/2:b'
    green = 'g>(r+b)/2?(r+b)/2:g'
    
    if i['temp_name3'].value() == '':
        i.knob('expr0').setValue('r')
        i.knob('expr1').setValue(green)
        i.knob('expr2').setValue('b')
        i.knob('expr3').setValue('a')
        i['label'].setValue('g: [value expr1]')
        
        i['temp_name3'].setValue('green_set')
        
        r = int(105)
        g = int(139)
        b = int(114)
        hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)
        i.knob("tile_color").setValue(int(hexColor))
    
    elif i['temp_name3'].value() == 'green_set':
        i.knob('expr0').setValue('r')
        i.knob('expr1').setValue('g')
        i.knob('expr2').setValue(blue)
        i.knob('expr3').setValue('a')
        i['label'].setValue('g: [value expr2]')
        
        i['temp_name3'].setValue('')
        
        r = int(66)
        g = int(97)
        b = int(109)
        hexColor = int("%02x%02x%02x%02x" %(r,g,b,1),16)
        i.knob("tile_color").setValue(int(hexColor))
