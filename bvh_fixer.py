bl_info = {
    "name": "BVH Fixer",
    "description": "This Add-On provides the ability to fix in place BVH Motion Capture files",
    "author": "Vinicius Guerrero & Thiago Bruno",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "BVH Fixer"
}

import bpy
import glob

from bpy.props import (StringProperty, PointerProperty)
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

# ------------------------------------------------------------------------
#    Addon Scene Properties
# ------------------------------------------------------------------------

class AddonProperties(PropertyGroup):

    target_name: StringProperty(
        name="Target", 
        description="Select the render target you want the files to be generated from", 
        maxlen=1024,
        subtype='DIR_PATH'
    ) 

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_FIXBVH(Operator):
    bl_idname = "wm.fix_bvh"
    bl_label = "Fix BVHs"
    bl_description = "Fix BVH Files To Stay In Place"

    def execute(self, context):
        
        scene = context.scene
        tool = scene.my_tool
        path = tool.target_name + "/*.bvh"
        bvhFiles = glob.glob(path)
        bvhFiles.sort()

        for fl in bvhFiles:
            fiIn = open(fl).readlines()
            export = open(str(fl.replace('.bvh', '') + "_inplace.bvh"), "w")
            ct = 0
            fX = 0.0
            fZ = 0.0
            for lines in fiIn:
                if ct in [0,1,2,3]:
                    export.write(lines)
                if "MOTION" in lines:
                    ct = 1
                if ct>0:
                    ct = ct + 1
                if ct > 4:
                    if ct == 4:
                        fX = float(lines.split(' ')[0])
                        fZ = float(lines.split(' ')[2])
                    lm = ''
                    col = 0
                    for x in lines.split(' '):        
                        if col == 0:
                            x = 0.0 # float(x) - fX
                        if col == 2:
                            x = 0.0 # float(x) - fZ
                        if lm == '':
                            lm = lm + str(x)
                        else:
                            lm = lm + ' ' + str(x)
                        col = col + 1
                    export.write(str(lm))
            export.close()
        
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "object.custom_panel"
    bl_label = "BVH Fixer"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "BVH Fixer"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.my_tool
        
        # Render Settings
        row = layout.row()
        box = layout.box()
        row = box.row()
        row.label(text="BVHs Location", icon='WORLD_DATA')
        row = box.row()
        row.separator()
        row = box.row()
        row.prop(tool, "target_name")
        layout.operator("wm.fix_bvh", icon="SCENE")
        row = layout.row() 

# ------------------------------------------------------------------------
#    Addon Registration
# ------------------------------------------------------------------------

classes = (AddonProperties, WM_OT_FIXBVH, OBJECT_PT_CustomPanel)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=AddonProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()