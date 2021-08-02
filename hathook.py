import cadquery as cq

hook_width = 12.0
hook_thickness = 4.0
clamp_depth = 25.0
corner_radius = 2.0

shelf_height = 8.0

hook = (
    cq.Workplane("XY")
      .rect(hook_width, clamp_depth+hook_thickness)
      .extrude(shelf_height + 2*hook_thickness)
)

hook = hook.edges("|Y").fillet(corner_radius)
hook = hook.edges(">Y").fillet(corner_radius)
hook = hook.edges("<Y").fillet(corner_radius)

shelf = (
    hook.faces('<Z')
        .workplane(hook_thickness, invert=True)
        .center(0, -hook_thickness)
        .rect(hook_width, clamp_depth)
        .extrude(shelf_height, combine=False)
)

hook = hook.cut(shelf)

# hook = hook.edges("|X").fillet(corner_radius)

cq.exporters.export(hook, 'hathook.stl')