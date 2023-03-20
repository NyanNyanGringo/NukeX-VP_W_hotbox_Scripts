import os
import platform
import subprocess


operatingSystem = platform.system()

for i in nuke.selectedNodes():
     
    path_file = i.knob('file').value()
    
    
    if path_file.endswith("mov") or path_file.endswith("mp4"):
        path_open =  os.path.normpath(path_file)
    else:
        path_open =  os.path.normpath(os.path.dirname(path_file))


    if os.path.exists(path_open):

        if operatingSystem == "Windows":
            subprocess.call(("explorer", "/select,", path_open))
        elif operatingSystem == "Darwin":
            subprocess.call(["open", "-R", path_open])
        else:
            subprocess.call(["nautilus", "--select", path_open])
