import cadquery as cq

hook_width = 12.0
hook_thickness = 4.0
clamp_depth = 25.0
shelf_height = 20.0
corner_radius = 3.0

hook = (
    cq.Workplane("XY")
      .rect(hook_width+hook_thickness, clamp_depth)
      .extrude(shelf_height + 2*hook_thickness)
)

shelf = (
    hook.faces('>Z')
        .workplane(-hook_thickness, True)
        .rect(clamp_depth, hook_width)
        .extrude(shelf_height, False)
)

hook = hook.cut(shelf)

# hook = hook.edges("|Y").fillet(corner_radius)
# hook = hook.edges("|X").fillet(corner_radius)

cq.exporters.export(hook, 'hathook.stl')