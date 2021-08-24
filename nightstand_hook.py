import cadquery as cq

hook_width = 12.0
hook_id = 30.0
clip_height = 20.0
clip_depth = 30.0
thickness = 4.0


pinch_val = 1.5

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
      .threePointArc((0, -(hook_id/2)-thickness), (hook_id, 0))
      .close()
      .extrude(hook_width)
)

hanger_cut = (
    cq.Workplane("XY")
      .center(clip_depth+thickness, -thickness+1)
      .threePointArc((thickness, -(hook_id/2)-(thickness)), (hook_id-(2*thickness), 0))
      .close()
      .extrude(hook_width)
)

hook = hook.union(hanger)
hook = hook.edges("|Z").fillet(1.5)
hook = hook.cut(hanger_cut)


cq.exporters.export(hook, 'nightstand.stl')