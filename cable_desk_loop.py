import cadquery as cq

hook_width = 18.0
hook_id = 50.0
clip_height = 19.5 # Fits tight on a 20mm board
clip_depth = 30.0
thickness = 4.0


pinch_val = 2.0

clipcut = (
    cq.Workplane("XY")
      .lineTo(0, clip_height)
      .lineTo(clip_depth, clip_height)
      .lineTo(clip_depth, 0)
      .lineTo(0, pinch_val)
      .close()
      .extrude(hook_width)
)

clip = (
    cq.Workplane("XY")
      .lineTo(0, clip_height+thickness)
      .lineTo(clip_depth+thickness, clip_height+thickness)
      .lineTo(clip_depth+thickness, -thickness)
      .lineTo(0, -thickness)
      .close()
      .extrude(hook_width)
)

# hook = hook.union(clip)
hook = clip.cut(clipcut)

hanger = (
    cq.Workplane("XY")
      .center(clip_depth-3, -thickness)
      # .threePointArc((0, -(hook_id/2)-thickness), (hook_id, 0))
      .threePointArc((0, -(hook_id/2)-thickness), (hook_id-20, 20))
      .close()
      .extrude(hook_width)
)

hanger_cut = (
    cq.Workplane("XY")
      .center(clip_depth+thickness, -thickness+1)
      .threePointArc((thickness, -hook_id/2-(thickness+3)), (hook_id-thickness-10, 0))
      .close()
      .extrude(hook_width)
      # .center(clip_depth-3, -thickness)
      # .rect(50, -15).extrude(hook_width)
)

hook = hook.union(hanger)
# hook = hook.edges("|Z").fillet(1.5)
hook = hook.cut(hanger_cut)
# hook = hook.faces(">X").edges(">Y").fillet(3)

cq.exporters.export(hook, 'desk_loop.stl')