import hou
import sys, os

hip_file = sys.argv[1]
input_file = sys.argv[2]
input_file_strip = os.path.splitext(input_file)[0]

hou.hipFile.load(hip_file)

file_node = hou.node("/obj/geo1/file1")
file_node.parm("file").set(input_file)

name_node = hou.node("/obj/geo1/set_name")
name_node.parm("name").set(input_file_strip)

export_node = hou.node('/obj/geo1/filecache1')
export_node.parm("file").set(input_file_strip + "_remeshed.bgeo.sc")
export_node.parm("execute").pressButton()
