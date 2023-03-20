import nuke


def copyWithClear(node=None):
    for name, knob in node.knobs().items():
        try:
            if knob.isAnimated():
                knob.clearAnimated()
        except AttributeError:
            pass

for i in nuke.selectedNodes():
    copyWithClear(i)
