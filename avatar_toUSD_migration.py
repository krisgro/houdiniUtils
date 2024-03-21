import hou
import os

class USDmigrationUtils:
    def __init__(self, dir_path):
        self.dir_path = dir_path
        
    def test(self):
        print("Hello World")

    def importAvatar(self):
        self.glb_file = [file for file in os.listdir(self.dir_path) if file.endswith(".glb")][0]
        
        self.asset_name = self.glb_file[:-4]
        print(self.asset_name)
        
        #gltf hierarchy creation
        self.obj_path = "/obj"
        glbcreate_sop = hou.node(self.obj_path).createNode("gltf_hierarchy", self.asset_name)
        glbcreate_sop.parm("filename").set(self.dir_path + "/" + self.glb_file)
        glbcreate_sop.parm("flattenhierarchy").set(1)
        glbcreate_sop.parm("importcustomattributes").set(0)
        glbcreate_sop.parm("buildscene").pressButton()

    def stageMaterials(self, input):
        #material lop
        materiallib_lop = input.createOutputNode("materiallibrary")
        materiallib_lop.parm("matflag1").set(0)
        materiallib_lop.parm("matnet").set(f"{self.obj_path}/{self.asset_name}/materials")
        materiallib_lop.parm("materials").set(0)
        materiallib_lop.parm("fillmaterials").pressButton()
        
        #get number of shaders in asset
        materials_num = materiallib_lop.parm("materials").eval()
        #init empty list
        materials = []
        #add shader names into a list
        for i in range(materials_num):
            temp = materiallib_lop.parm(f"matpath{i+1}").eval()
            materials.append(temp)

            #link paths
            materiallib_lop.parm(f"geopath{i+1}").set(f"/avtr_{self.asset_name}/avatar/{temp}")
            materiallib_lop.parm(f"matpath{i+1}").set(f"/avtr_{self.asset_name}/materials/{temp}")

        self.to_rop = materiallib_lop

    def createStage(self):
        #sopcreate lop
        root_path = "/stage"
        sopcreate_lop = hou.node(root_path).createNode("sopcreate", "avatar")
        sopcreate_lop.parm("enable_partitionattribs").set(0)

        #gltf sop
        gltf_sop = hou.node(sopcreate_lop.path() + "/sopnet/create").createNode("gltf", "IN_avatar")
        gltf_sop.parm("filename").set(self.dir_path + "/" + self.glb_file)
        gltf_sop.parm("pointconsolidatedist").set("0.0001")
        gltf_sop.parm("usecustomattribs").set(0)
        gltf_sop.parm("materialassigns").set(1)
        gltf_sop.moveToGoodPosition()
       
        #compiled for-loop //BEGIN
        compile_begin = gltf_sop.createOutputNode("compile_begin", "compile_begin1")
        compile_begin.parm("blockpath").set("../compile_end1")
        compile_begin.moveToGoodPosition()
       
        for_each_begin = compile_begin.createOutputNode("block_begin", "foreach_begin1")
        for_each_begin.parm("method").set(1)
        for_each_begin.parm("blockpath").set("../foreach_end1")
        for_each_begin.moveToGoodPosition()
        
        #attribute wrangle
        attr_wrangle = for_each_begin.createOutputNode("attribwrangle", "set_path")
        attr_wrangle.parm("class").set(1)
        attr_wrangle.parm("snippet").set('\nstring list[] = split(s@shop_materialpath, "/");\ns@path = "/" + list[-1];')
        attr_wrangle.moveToGoodPosition()

        #compiled for-loop //END
        for_each_end = attr_wrangle.createOutputNode("block_end", "foreach_end1")
        for_each_end.parm("itermethod").set(1)
        for_each_end.parm("method").set(1)
        for_each_end.parm("class").set(0)
        for_each_end.parm("useattrib").set(1)
        for_each_end.parm("attrib").set("shop_materialpath")
        for_each_end.parm("blockpath").set("../foreach_begin1")
        for_each_end.parm("templatepath").set("../foreach_begin1")
        for_each_end.parm("multithread").set(1)
        for_each_end.moveToGoodPosition()

        compile_end = for_each_end.createOutputNode("compile_end", "compile_end1")
        compile_end.moveToGoodPosition()

        #attrib delete
        att_delete = compile_end.createOutputNode("attribdelete")
        att_delete.parm("vtxdel").set("* ^N ^uv")
        att_delete.parm("primdel").set("* ^path")
        att_delete.parm("dtldel").set("*")
        att_delete.moveToGoodPosition()

        #output sop
        output_sop = att_delete.createOutputNode("output")
        output_sop.moveToGoodPosition()

        #create primitive lop
        primitive_lop = hou.node(root_path).createNode("primitive")
        primitive_lop.parm("primpath").set("avtr_" + self.asset_name)
        primitive_lop.parm("primkind").set("component")

        #graft stages
        graft_stages_lop = primitive_lop.createOutputNode("graftstages")
        graft_stages_lop.setNextInput(sopcreate_lop)
        graft_stages_lop.parm("primkind").set("subcomponent")

        #Layout Nodes
        primitive_lop.moveToGoodPosition()
        sopcreate_lop.moveToGoodPosition()
        graft_stages_lop.moveToGoodPosition()

        #stageMats method
        self.stageMaterials(graft_stages_lop)

        #usd rop export
        usd_rop_export = self.to_rop.createOutputNode("usd_rop")
        usd_rop_export.parm("lopoutput").set(self.dir_path + "/usd_export/" + self.asset_name + ".usd") #change suffix to .usdz for full houdini lic
        usd_rop_export.parm("execute").pressButton()

    def run(self):
        self.importAvatar()
        self.createStage()