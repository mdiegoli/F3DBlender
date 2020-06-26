bl_info = {
    'name': 'Monkey Grid',
    'author': 'dr. Sybren',
    'version': (2, 0, 0),
    'blender': (2, 81, 0),
    'location': 'Mesh → Add',
    'description': 'Allows easy monkification',
    'category': 'Add Mesh',
}


import bpy

def monkey_grid(count_x: int, count_y: int, distance: float) -> bool:
    """Create a grid of monkeys.

    :param count_x: number of monkeys in X-direction
    :param count_y: number of monkeys in Y-direction
    :param distance: blender units between centres of monkeys.

    NOTE: This function changes selection and active object context.
    """

    for idx in range(count_x * count_y):
        x = idx % count_x * distance
        y = idx // count_x * distance

        result = bpy.ops.mesh.primitive_monkey_add(
            size=0.4, location=(x, y, 1))
        if 'FINISHED' not in result:
            return False
    return True

# https://docs.blender.org/api/master/bpy.types.Operator.html
class MESH_OT_monkey_grid(bpy.types.Operator):
    bl_idname = 'mesh.monkey_grid'
    bl_label = 'Monkey Grid'
    bl_description = 'Creates a horizontal grid of tiny monkeys'
    bl_options = {'REGISTER', 'UNDO'}

    # https://docs.blender.org/api/master/bpy.props.html
    count_x: bpy.props.IntProperty(name='Count X', default=3, min=1, soft_max=10)
    count_y: bpy.props.IntProperty(name='Count Y', default=2, min=1, soft_max=10)
    distance: bpy.props.FloatProperty(
        name='Distance', default=1.0,
        soft_min=0.1, soft_max=2.0,
        subtype='DISTANCE', unit='LENGTH')

    def execute(self, context):
        ok = monkey_grid(self.count_x, self.count_y, self.distance)
        if not ok:
            return {'CANCELLED'}
        return {'FINISHED'}


class VIEW3D_PT_monkeys(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Ubisoft"
    bl_label = "Monkeys"

    def draw(self, context) -> None:
        layout = self.layout

        col = layout.column(align=True)
        col.prop(context.window_manager, 'mg_count_x')
        col.prop(context.window_manager, 'mg_count_y')
        col.prop(context.window_manager, 'mg_distance')
        props = col.operator('mesh.monkey_grid', text="Grid")
        props.count_x = context.window_manager.mg_count_x
        props.count_y = context.window_manager.mg_count_y
        props.distance = context.window_manager.mg_distance


def draw_on_add_menu(self, context):
    # self.layout.operator(MESH_OT_monkey_grid.bl_idname,
    #                      text='GRID OF MONKAYS')
    self.layout.menu("VIEW3D_MT_mesh_add")

classes = (
    MESH_OT_monkey_grid,
    VIEW3D_PT_monkeys,
)
cls_register, cls_unregister = bpy.utils.register_classes_factory(classes)

def register():
    cls_register()
    bpy.types.TOPBAR_MT_editor_menus.append(draw_on_add_menu)

    bpy.types.WindowManager.mg_count_x = bpy.props.IntProperty(name='Count X', default=3, min=1, soft_max=10)
    bpy.types.WindowManager.mg_count_y = bpy.props.IntProperty(name='Count Y', default=2, min=1, soft_max=10)
    bpy.types.WindowManager.mg_distance = bpy.props.FloatProperty(
        name='Distance', default=1.0,
        soft_min=0.1, soft_max=2.0,
        subtype='DISTANCE', unit='LENGTH')


def unregister():
    cls_unregister()
    bpy.types.TOPBAR_MT_editor_menus.remove(draw_on_add_menu)

    del bpy.types.WindowManager.mg_count_x
    del bpy.types.WindowManager.mg_count_y
    del bpy.types.WindowManager.mg_distance
