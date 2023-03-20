import nuke
import nukescripts
import os, re


class Panel(nukescripts.PythonPanel):
    def __init__(self, write):
        nukescripts.PythonPanel.__init__(self, 'Fast Export: Prerender')

        # print(dir(self))

        self.can_I_render = False
        self.write = write

        # changeable variables
        self.var1 = "prerenders"

        # variables
        self.all_ok = False
        self.root = os.path.split(nuke.root().name())[0]
        self.extensions = ["dpx", "exr", "hdr", "jpeg", "mov", "png", "tiff", "mp4"]
        
        # construct
        self.read_file, self.read_ext, self.read_cc = self.getReadValues()
        self.setupUI()
        self.setPanelKnobValues()
        self.showModal()

    def start(self):
        return self.can_I_render

    def setupUI(self):
        self.p_name = nuke.String_Knob("p_name", "Prerender name:", "")
        self.addKnob(self.p_name)

        self.p_fakeok = nuke.PyScript_Knob("p_fakeok", "Render!")
        self.addKnob(self.p_fakeok)
        self.p_fakeok.clearFlag(nuke.STARTLINE)
        self.p_fakeok.setVisible(False)

        self.p_ok = nuke.PyScript_Knob("p_ok", "Render!")
        self.addKnob(self.p_ok)
        self.p_ok.clearFlag(nuke.STARTLINE)
        self.p_ok.setEnabled(False)

        self.p_div0 = nuke.Text_Knob('', '', ' ')
        self.addKnob(self.p_div0)

        self.p_ext = nuke.Enumeration_Knob("p_ext", "Extension:", self.extensions)
        self.addKnob(self.p_ext)
        self.p_ext.setFlag(nuke.STARTLINE)
        self.p_ext.setEnabled(False)

        self.p_cc = nuke.Enumeration_Knob("p_cc", "Colorspace:", [])
        self.addKnob(self.p_cc)
        self.p_cc.clearFlag(nuke.STARTLINE)
        self.p_cc.setEnabled(False)

        self.p_first = nuke.Int_Knob("p_first", "First:")
        self.addKnob(self.p_first)
        self.p_first.clearFlag(nuke.STARTLINE)
        self.p_first.setEnabled(False)

        self.p_last = nuke.Int_Knob("p_last", "Last:")
        self.addKnob(self.p_last)
        self.p_last.clearFlag(nuke.STARTLINE)
        self.p_last.setEnabled(False)

        self.p_fps = nuke.Int_Knob("p_fps", "FPS:")
        self.addKnob(self.p_fps)
        self.p_fps.clearFlag(nuke.STARTLINE)
        self.p_fps.setEnabled(False)
        self.p_fps.setVisible(False)

        self.p_div1 = nuke.Text_Knob('', '', ' ')
        self.addKnob(self.p_div1)

        self.p_log = nuke.Multiline_Eval_String_Knob("p_log", "Prerender folder files:", "")
        self.addKnob(self.p_log)
        self.p_log.setFlag(nuke.STARTLINE)
        # self.p_log.setEnabled(False)

        self.setMinimumSize(950, 500)

    def knobChanged(self, knob):
        if knob is self.p_name:
            self.setEnabledDisabled()
        if knob is self.p_log:
            self.setLogKnobValues()
        if knob is self.p_ok:
            self.setWriteValues()
        if knob is self.p_ext:
            if knob.value() == "mov" or knob.value() == "mp4":
                self.p_fps.setVisible(True)
            else:
                self.p_fps.setVisible(False)

    def setEnabledDisabled(self):
        if self.p_name.value() == "":
            self.p_ok.setEnabled(False)
            self.p_ext.setEnabled(False)
            self.p_cc.setEnabled(False)
            self.p_first.setEnabled(False)
            self.p_last.setEnabled(False)
            self.p_fps.setEnabled(False)
        else:
            self.p_ok.setEnabled(True)
            self.p_ext.setEnabled(True)
            self.p_cc.setEnabled(True)
            self.p_first.setEnabled(True)
            self.p_last.setEnabled(True)
            self.p_fps.setEnabled(True)

    def getReadValues(self):
        topnode_file = nuke.tcl("value [topnode %s].file" % self.write.name())
        topnode_endswith = topnode_file.split(".")[-1]
        topnode_colorspace = nuke.tcl("value [topnode %s].colorspace" % self.write.name())
        topnode_colorspace = topnode_colorspace.replace("default (", "").replace(")", "")

        return topnode_file, topnode_endswith, topnode_colorspace

    def setPanelKnobValues(self):

        # Set extension
        self.p_ext.setValue(self.read_ext)

        # Set colospace
        tempWrite = nuke.nodes.Write()
        colospaces = tempWrite['colorspace'].values()
        nuke.delete(tempWrite)
        self.p_cc.setValues(colospaces)
        self.p_cc.setValue(self.read_cc)

        # Set First and Last
        self.p_first.setValue(self.write.firstFrame())
        self.p_last.setValue(self.write.lastFrame())

        # Set FPS
        topnode_name = nuke.tcl("value [topnode %s].name" % write.name())
        metadate = nuke.toNode(topnode_name).metadata()
        for key, value in metadate.items():
            if "frame_rate" in key:
                self.p_fps.setValue(int(value))
        if self.p_ext.value() == "mov" or self.p_ext.value() == "mp4":
                self.p_fps.setVisible(True)
        else:
            self.p_fps.setVisible(False)

        # Set log
        self.setLogKnobValues()

    def setLogKnobValues(self):
        path = os.path.join(self.root, self.var1)
        if os.path.exists(path):
            files = os.listdir(path)
            self.p_log.setValue(str("\n".join(files)))
        else:
            self.p_log.setValue("Prerender directory not created.")

    def setWriteValues(self):
        # values for write
        prerender_path = os.path.join(self.root, self.var1)
        if self.p_ext.value() == "mov" or self.p_ext.value() == "mp4":
            file_type = "mov"
            path = os.path.join(prerender_path, self.p_name.value() + "." + file_type)
        else:
            file_type = self.p_ext.value()
            path = os.path.join(prerender_path, self.p_name.value())
            path = os.path.join(path, self.p_name.value() + ".####." + file_type)
            
        if not self.checkFileExists(path) and nuke.ask("Start render?"):
            # set values to write
            self.write.resetKnobsToDefault()
            self.write['file'].setValue(path.replace("\\", "/"))
            self.write['file_type'].setValue(file_type)
            self.write['colorspace'].setValue(self.p_cc.value())
            self.write['create_directories'].setValue("1")
            self.write['first'].setValue(self.p_first.value())
            self.write['last'].setValue(self.p_last.value())
            self.write['channels'].setValue("all")
            if file_type == "mov":
                self.write["mov_prores_codec_profile"].setValue("ProRes 4:4:4:4 12-bit")
                self.write["mov64_fps"].setValue(self.p_fps.value())

            self.can_I_render = True
            self.finishModalDialog(True)

    def checkFileExists(self, path_to_file):

        if self.p_ext.value() == "mov" or self.p_ext.value() == "mp4":

            if os.path.exists(path_to_file):
                if nuke.ask('Prerender with name ' + self.p_name.value() + ' already exists! Rewrite?'):
                    return False
                else:
                    return True
            else:
                return False

        else:

            if os.path.exists(os.path.split(path_to_file)[0]):
                if nuke.ask('Prerender with name ' + self.p_name.value() + ' already exists! Rewrite?'):
                    return False
                else:
                    return True
            else:
                return False


### CHECK BEFORE START QT ###


writes = []
for write in nuke.selectedNodes():
    writes.append(write)

check = 0
if check == 0:
    if len(writes) == 1:
        check += 1
        write = writes[0]
    else:
        nuke.message("Please select only one Write node!")

if check == 1:
    if nuke.root().name() != 'Root':
        check += 1
    else:
        nuke.message("Please save project first!")

if check == 2:
    if write.inputs() == 1:
        check += 1
    else:
        nuke.message("Please connect input to write!")

if check == 3:
    topnode_name = nuke.tcl("value [topnode %s].name" % write.name())
    if nuke.toNode(topnode_name).Class() == "Read":
        check += 1
    else:
        nuke.message("Topnode is not Read!")


### START ###


if check == 4:
    p = Panel(writes[0])
    ok = p.start()
    if ok:
        nuke.execute(writes[0], int(writes[0].knob('first').value()), int(writes[0].knob('last').value()))
        nuke.message("Render finished!")
