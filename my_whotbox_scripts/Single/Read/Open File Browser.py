import os
import platform
import subprocess
import webbrowser


operatingSystem = platform.system()


for node in nuke.selectedNodes():
    file = node.knob('file')
    file_val = file.value()

    if file_val.endswith("mov") or file_val.endswith("mp4"):
        openPath =  os.path.normpath(file_val)
    else:
        openPath =  os.path.normpath(os.path.dirname(file_val))

    if os.path.exists(openPath):
        if operatingSystem == "Windows":
            subprocess.call(("explorer", "/select,", openPath))
        elif operatingSystem == "Darwin":
            subprocess.call(["open", "-R", openPath])
        else:
            subprocess.call(["nautilus", "--select", openPath])
    else:
        nuke.message("My Master, no path \n\n" + openPath)
