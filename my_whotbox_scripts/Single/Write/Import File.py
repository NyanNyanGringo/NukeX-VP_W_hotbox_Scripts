import os
import nuke
import re


MOV_EXTENSIONS = [".mov", ".mp4"]
SEQUENCE_EXNTENSIONS = [".exr", ".dpx", ".png", ".tiff", ".psd", ".jpeg", ".jpg"]
EXTENSIONS = MOV_EXTENSIONS + SEQUENCE_EXNTENSIONS


# STRING HELPERS


def get_start_end_indexes(where_search, what_search):
    if find := re.finditer(what_search, where_search):
        return [(m.start(0), m.end(0)) for m in find]


def replace_on_end(what_replace: str, for_what_replace: str, where_replace: str, _on_start=False) -> str:
    """
    Work as classic replace but only for one element in the end of string
    """
    if indexes := get_start_end_indexes(where_replace, what_replace):
        index_in, index_out = indexes[-1]
        string = "".join([where_replace[:index_in], for_what_replace, where_replace[index_out:]])
        return string
    return where_replace


def get_file_extension(file_path):
    """Return file extension (with dot), if it is supported and exists"""
    try:
        file_extension = "." + file_path.split(".")[-1]
    except IndexError as e:
        message = f"Can't get file extension: {e}"
        nuke.message(message)
        raise IndexError(message)

    if file_extension not in EXTENSIONS:
        message = f"Not supported extension: {file_extension}. Supported: " + ", ".join(EXTENSIONS)
        nuke.message(message)
        raise ValueError(message)

    return file_extension


def file_is_sequence(file_path: str) -> bool:
    file_extension = get_file_extension(file_path)

    if file_extension in MOV_EXTENSIONS:
        return False
    return True


def get_file_name(file_full_name: str) -> str:
    """Return file name without extension and version"""
    file_extension = get_file_extension(file_full_name)

    # remove extension
    file_name = replace_on_end(file_extension, "", file_full_name)

    # remove %d или %00d или .####
    file_name = re.sub("%(\d+|)d", "", file_name)
    file_name = re.sub("\.#+", "", file_name)

    # remove version
    file_name = re.sub("_v\d+", "", file_name)

    # remove dots in the end if exists
    return re.sub("\.+$", "", file_name)


# NUKE HELPERS


def convert_tcl(tcl_code: str, node: nuke.Node = None, return_all_string: bool = True) -> str:
    """
    Convert TCL code to Python and execute it.

    :param tcl_code: ...
    :param node: node which contains this TCL code.
    :param return_all_string: if False, return TCL code without any other string.
    :return: result of TCL code after executing.
    """
    if node:  # convert TCL "topnode" command
        tcl_code = tcl_code.replace("[topnode]", f"[topnode {node.name()}]")
        tcl_code = tcl_code.replace("[topnode this", f"[topnode {node.name()}")
        tcl_code = tcl_code.replace("[topnode input", f"[topnode {node.name()}.input")
        tcl_code = tcl_code.replace("[topnode parent", f"[topnode {node.name()}.parent")

    if return_all_string:
        return nuke.tcl("subst", tcl_code)
    return nuke.tcl(tcl_code)


def set_colorspace_from_write_to_read(write_node, read_node):
    write_colorspace = write_node["colorspace"].value()

    if "default (" in write_colorspace:
        read_node["colorspace"].setValue(0)
        return

    read_node["colorspace"].setValue(write_colorspace)


# OS HELPERS


def check_path_exists(file_path: str) -> bool:

    if not file_path:
        return False

    if get_file_extension(file_path) in MOV_EXTENSIONS and not os.path.exists(file_path):
        return False

    if get_file_extension(file_path) in SEQUENCE_EXNTENSIONS and not os.path.exists(os.path.dirname(file_path)):
        return False

    return True


# START


def start():
    for write_node in nuke.selectedNodes():
        file_path = write_node.knob('file').value()
        file_path = convert_tcl(file_path, write_node)

        if not check_path_exists(file_path):
            nuke.message(f"File doesn't exists:\n\n{file_path}")
            return

        if file_is_sequence(file_path):

            file_dir = os.path.dirname(file_path)
            file_full_name = os.path.basename(file_path)
            file_name = get_file_name(file_full_name)
            file_extension = get_file_extension(file_full_name)

            nuke_file_name = str()
            for f in nuke.getFileNameList(file_dir):

                if not file_extension in f:
                    continue
                if not file_name in f:
                    continue

                nuke_file_name = f

            assert nuke_file_name, f"Unsuspected Error!"
            nuke_file_path = os.path.join(file_dir, nuke_file_name).replace("\\", "/")

            regexp_pattern = " \d+-\d+$"
            more_than_one_file_in_sequence = re.findall(regexp_pattern, nuke_file_name)
            if more_than_one_file_in_sequence:
                frame_range = re.findall(regexp_pattern, nuke_file_name)[0]
                read_node = nuke.nodes.Read(file=re.split(regexp_pattern, nuke_file_path)[0],
                                       first=frame_range.split("-")[0],
                                       last=frame_range.split("-")[1])
            else:
                read_node = nuke.createNode('Read', "file {" + nuke_file_path + "}", inpanel=False)

            set_colorspace_from_write_to_read(write_node, read_node)

        else:
            read_node = nuke.createNode('Read', "file {" + file_path + "}", inpanel=False)

        read_node.setXpos(write_node.xpos())
        read_node.setYpos(write_node.ypos() + 100)


if __name__ == "W_hotbox":
    start()
