import os


def check_for_right_endswitch(string, keys):
    for key in keys:
        if string.endswith(key):
            return True
            break
            
def file_exists(file_path):
    os.path.exists(file_path)

endswitches = ['exr', 'dpx', 'png', 'tiff', 'mov', 'mp4', 'psd', 'jpeg', 'jpg']

for i in nuke.selectedNodes():
    file = i.knob('file').value()
    
    if check_for_right_endswitch(file, endswitches) and os.path.split(file)[0]:
        
        if file.endswith("mov") or file.endswith("mp4"):
            colorspace = 'sRGB'
            read = nuke.createNode('Read', "file {"+file+"}", inpanel = False)
        
        else:
            all_files = os.listdir(os.path.dirname(file))
            right_files = []
            for q in all_files:
                if check_for_right_endswitch(q, endswitches):
                    right_files.append(q)
            files_amount = len(right_files)
            first_file = str(right_files[0])
            first_file_split = first_file.rsplit(".")
            first = int(first_file_split[-2])
            last = first + (files_amount-1)
            
            colorspace = i.knob('colorspace').value()
            colorspace = colorspace.replace("default (", "").replace(")", "")
            
            read = nuke.nodes.Read(file=file, colorspace=colorspace, first=first, last=last)
        
        read.setXpos(i.xpos())
        read.setYpos(i.ypos() + 100)
        
    else:
        nuke.message('Be sure that file has right extension')
