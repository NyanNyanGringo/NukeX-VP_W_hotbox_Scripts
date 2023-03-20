# indexes:
# 0 is left | 1 is right | 2 is top
# 3 is bot | 4 is left_bot | 5 is left_top
# 6 is right_bot | 7 is right_top

index = 0

for i in nuke.selectedNodes():
    left = [-1, 0, 1,
            -1, 0, 1,
            -1, 0, 1]
    right = [1, 0, -1,
             1, 0, -1,
             1, 0, -1]
    top = [-1, -1, -1, 
            0, 0, 0, 
            1, 1, 1]
    bot = [1, 1, 1, 
           0, 0, 0, 
          -1, -1, -1]
    left_bot = [0, 1, 1, 
               -1, 0, 1, 
               -1, -1, 0]
    left_top = [-1, -1, 0, 
                -1, 0, 1, 
                 0, 1, 1]
    right_bot = [1, 1, 0, 
                 1, 0, -1, 
                 0, -1, -1]
    right_top = [0, -1, -1, 
                 1, 0, -1, 
                 1, 1, 0]

    index_compare = ["left", "right", "top", "bot", "left_bot", "left_top", "right_bot", "right_top"]
    
    counter = 0
    for v in eval(index_compare[index]):
        i['matrix'].setValue(v, counter)
        counter += 1
