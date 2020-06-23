import bpy

bpy.ops.curve.primitive_bezier_curve_add()

c = bpy.context.object

c.data.resolution_u     = 24     # Preview U
c.data.fill_mode        = 'FULL' # Fill Mode ==> Full
c.data.bevel_depth      = 0.02   # Bevel Depth
c.data.bevel_resolution = 4      # Bevel Resolution
