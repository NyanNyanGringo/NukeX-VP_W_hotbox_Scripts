import os
import platform
import subprocess


operatingSystem = platform.system()
root_name = nuke.root().name()
openPath = os.path.normpath(root_name)

if os.path.exists(openPath) and root_name != 'Root':
    if operatingSystem == "Windows":
        subprocess.call(("explorer", "/select,", openPath))
    elif operatingSystem == "Darwin":
        subprocess.call(["open", "-R", openPath])
    else:
        subprocess.Popen(["xdg-open", openPath])
else:
    nuke.message("My Master, no path \n\n" + openPath)
