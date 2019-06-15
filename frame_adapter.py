bl_info = {
    "name": "Frame Adapter",
    "description": "This Add-On provides the ability to adapt timeline end frame to current action end frame size",
    "author": "Vinicius Guerrero & Thiago Bruno",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Frame Adapter"
}

import bpy
import glob

from bpy.props import (StringProperty, PointerProperty)
from bpy.types import (Panel, Menu, Operator, PropertyGroup)

# ------------------------------------------------------------------------
#    Addon Scene Properties
# ------------------------------------------------------------------------

class AddonProperties(PropertyGroup):
    pass 

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_FrameAdapter(Operator):
    bl_idname = "wm.frame_adapter"
    bl_label = "Timeline Adapt"
    bl_description = "Adapts timeline end frame to current action end frame size"

    def execute(self, context):
        if bpy.data.actions:
            bpy.context.scene.frame_end=bpy.context.object.animation_data.action.frame_range[-1]
        return {'FINISHED'}
    
# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_idname = "object.custom_panel"
    bl_label = "Frame Adapter"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Frame Adapter"
    bl_context = "objectmode"   

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        tool = scene.my_tool
        
        # Render Settings
        layout.operator("wm.frame_adapter", icon="SCENE")
        row = layout.row() 

# ------------------------------------------------------------------------
#    Addon Registration
# ------------------------------------------------------------------------

classes = (AddonProperties, WM_OT_FrameAdapter, OBJECT_PT_CustomPanel)

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
