import nuke
import nukescripts
import os, re, shutil


unique_write_name = "WriteE847V309FG27E43"


class Panel(nukescripts.PythonPanel):
    def __init__(self, write):
        nukescripts.PythonPanel.__init__(self, 'Fast Export: Single Frame')

        # print(dir(self))

        self.can_I_render0 = False
        self.can_I_render1 = False
        self.write = write

        # changeable variables
        self.var1 = "single_frames"

        # variables
        self.all_ok = False
        self.root = os.path.split(nuke.root().name())[0]
        self.extensions = ["dpx", "exr", "hdr", "jpeg", "png", "tiff"]
        
        # construct
        self.read_file, self.read_ext, self.read_cc = self.getReadValues()
        self.setupUI()
        self.setPanelKnobValues()
        self.showModal()

    def start(self):
        return self.can_I_render0, self.can_I_render1

    def setupUI(self):
        self.p_name = nuke.String_Knob("p_name", "Single Frame name:", "")
        self.addKnob(self.p_name)

        self.p_fakeok = nuke.PyScript_Knob("p_fakeok", "Render!")
        self.addKnob(self.p_fakeok)
        self.p_fakeok.clearFlag(nuke.STARTLINE)
        self.p_fakeok.setVisible(False)

        self.p_frame = nuke.Int_Knob("p_frame", "")
        self.addKnob(self.p_frame)
        self.p_frame.clearFlag(nuke.STARTLINE)
        self.p_frame.setEnabled(False)

        self.p_ok = nuke.PyScript_Knob("p_ok", "Render!")
        self.addKnob(self.p_ok)
        self.p_ok.clearFlag(nuke.STARTLINE)
        self.p_ok.setEnabled(False)

        self.p_div0 = nuke.Text_Knob('', '', ' ')
        self.addKnob(self.p_div0)

        self.p_use_frame_in_name = nuke.Boolean_Knob("p_use_frame_in_name", "Show frames in files name?", "1")
        self.addKnob(self.p_use_frame_in_name)
        self.p_use_frame_in_name.setFlag(nuke.STARTLINE)
        self.p_use_frame_in_name.setEnabled(False)

        self.p_ext0 = nuke.Enumeration_Knob("p_ext0", "Preview", self.extensions)
        self.addKnob(self.p_ext0)
        self.p_ext0.setFlag(nuke.STARTLINE)
        self.p_ext0.setEnabled(False)

        self.p_cc0 = nuke.Enumeration_Knob("p_cc0", "", [])
        self.addKnob(self.p_cc0)
        self.p_cc0.clearFlag(nuke.STARTLINE)
        self.p_cc0.setEnabled(False)

        self.p_active0 = nuke.Boolean_Knob("p_active0", "", "1")
        self.addKnob(self.p_active0)
        self.p_active0.clearFlag(nuke.STARTLINE)
        self.p_active0.setEnabled(False)

        self.p_ext1 = nuke.Enumeration_Knob("p_ext1", "Hires", self.extensions)
        self.addKnob(self.p_ext1)
        self.p_ext1.setFlag(nuke.STARTLINE)
        self.p_ext1.setEnabled(False)

        self.p_cc1 = nuke.Enumeration_Knob("p_cc1", "", [])
        self.addKnob(self.p_cc1)
        self.p_cc1.clearFlag(nuke.STARTLINE)
        self.p_cc1.setEnabled(False)

        self.p_active1 = nuke.Boolean_Knob("p_active1", "", "1")
        self.addKnob(self.p_active1)
        self.p_active1.clearFlag(nuke.STARTLINE)
        self.p_active1.setEnabled(False)

        self.p_div1 = nuke.Text_Knob('', '', ' ')
        self.addKnob(self.p_div1)

        self.p_log = nuke.Multiline_Eval_String_Knob("p_log", "Prerender folder files:", "")
        self.addKnob(self.p_log)
        self.p_log.setFlag(nuke.STARTLINE)

        self.setMinimumSize(500, 500)

    def knobChanged(self, knob):
        if knob is self.p_name:
            self.setEnabledDisabled()
        if knob is self.p_active0 or knob is self.p_active1:
            self.setEnabledDisabledActive()
        if knob is self.p_log:
            self.setLogKnobValues()
        if knob is self.p_ok:
            self.setWriteValues()

    def setEnabledDisabledActive(self):
        if self.p_active0.value():
            self.p_ext0.setEnabled(True)
            self.p_cc0.setEnabled(True)
        else:
            self.p_ext0.setEnabled(False)
            self.p_cc0.setEnabled(False)

        if self.p_active1.value():
            self.p_ext1.setEnabled(True)
            self.p_cc1.setEnabled(True)
        else:
            self.p_ext1.setEnabled(False)
            self.p_cc1.setEnabled(False)

        if not self.p_active0.value() and not self.p_active1.value():
            self.p_ok.setEnabled(False)
        else:
            self.p_ok.setEnabled(True)

    def setEnabledDisabled(self):
        if self.p_name.value() == "":
            bool_val = False
        else:
            bool_val = True

        knobs = [self.p_frame, self.p_ok, self.p_ext0, self.p_cc0, self.p_active0,
        self.p_ext1, self.p_cc1, self.p_active1, self.p_use_frame_in_name]
        for knob in knobs:
            knob.setEnabled(bool_val)

        if not self.p_active0.value():
            self.p_ext0.setEnabled(False)
            self.p_cc0.setEnabled(False)
        if not self.p_active1.value():
            self.p_ext1.setEnabled(False)
            self.p_cc1.setEnabled(False)


    def getReadValues(self):
        topnode_file = nuke.tcl("value [topnode %s].file" % self.write.name())
        topnode_endswith = topnode_file.split(".")[-1]
        topnode_colorspace = nuke.tcl("value [topnode %s].colorspace" % self.write.name())
        topnode_colorspace = topnode_colorspace.replace("default (", "").replace(")", "")

        return topnode_file, topnode_endswith, topnode_colorspace

    def setPanelKnobValues(self):

        # Set frame
        self.p_frame.setValue(int(nuke.frame()))

        # Set extension
        self.p_ext0.setValue("png")
        if self.read_ext == "mov" or self.read_ext == "mp4":
            self.p_ext1.setValue("exr")
        else:
            self.p_ext1.setValue(self.read_ext)

        # Set colospace
        tempWrite = nuke.nodes.Write()
        colospaces = tempWrite['colorspace'].values()
        for cc in colospaces:
            if "sRGB" in cc:
                srgb_name = cc
                break
            else:
                srgb_name = "sRGB"
        nuke.delete(tempWrite)
        self.p_cc0.setValues(colospaces)
        self.p_cc1.setValues(colospaces)

        self.p_cc0.setValue(srgb_name)
        self.p_cc1.setValue(self.read_cc)

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
        single_frame_path = os.path.join(self.root, self.var1)
        file_subpath = os.path.join(single_frame_path, self.p_name.value())
        if self.p_use_frame_in_name.value():
            file_path0 = os.path.join(file_subpath, self.p_name.value() + "_prv.####." + self.p_ext0.value())
            file_path1 = os.path.join(file_subpath, self.p_name.value() + "_hires.####." + self.p_ext1.value())
        else:
            file_path0 = os.path.join(file_subpath, self.p_name.value() + "_prv." + self.p_ext0.value())
            file_path1 = os.path.join(file_subpath, self.p_name.value() + "_hires." + self.p_ext1.value())

        if not self.checkFileExists(file_subpath) and nuke.ask("Start render?"):
            write0 = self.write
            write0_input = write0.dependencies()[0]

            write1 = nuke.nodes.Write(name=unique_write_name)
            write1.setInput(0, write0_input)

            write0.resetKnobsToDefault()

            write0["file"].setValue(file_path0.replace("\\", "/"))
            write1["file"].setValue(file_path1.replace("\\", "/"))

            write0["file_type"].setValue(self.p_ext0.value())
            write1["file_type"].setValue(self.p_ext1.value())

            write0["colorspace"].setValue(self.p_cc0.value())
            write1["colorspace"].setValue(self.p_cc1.value())

            write0['create_directories'].setValue("1")
            write1['create_directories'].setValue("1")

            write0['first'].setValue(self.p_frame.value())
            write0['last'].setValue(self.p_frame.value())
            write1['first'].setValue(self.p_frame.value())
            write1['last'].setValue(self.p_frame.value())

            if self.p_active0.value():
                self.can_I_render0 = True
            if self.p_active1.value():
                self.can_I_render1 = True
            self.finishModalDialog(True)

    def checkFileExists(self, path_to_file):
        if os.path.exists(path_to_file):
            if nuke.ask('Prerender with name ' + self.p_name.value() + ' already exists! Rewrite?'):
                shutil.rmtree(path_to_file)
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
    ok0, ok1 = p.start()
    write1 = nuke.toNode(unique_write_name)
    if ok0:
        nuke.execute(write, int(write.knob('first').value()), int(write.knob('last').value()))
    if ok1:
        nuke.execute(write1, int(write1.knob('first').value()), int(write1.knob('last').value()))
    nuke.delete(write1)
    if ok0 or ok1:
        nuke.message("Render finished!")
