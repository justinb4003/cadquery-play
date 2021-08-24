import cadquery as cq

hook_id = 28
tiny_hook_id = 5
span = 120
thickness = 5
width = 8


bar = (
    cq.Workplane("XY")
      .rect(span, thickness)
      .extrude(width)
)

hook = (
    cq.Workplane("XY")
        .center(-span/2, -hook_id/2 - 0)
        .circle((hook_id+thickness) / 2.0)
        .extrude(width)
        .center(span, (hook_id/2)-(tiny_hook_id/2))
        .circle((tiny_hook_id+thickness) / 2.0)
        .extrude(width)
)

hook = bar.union(hook)


holes = (
    cq.Workplane("XY")
        .center(-span/2, -hook_id/2 - 0)
        .circle((hook_id) / 2.0)
        .extrude(width+20)
        .center(span, (hook_id/2)-(tiny_hook_id/2))
        .circle((tiny_hook_id) / 2.0)
        .extrude(width)
)

hook = hook.cut(holes)

big_cut = (
    cq.Workplane("XY")
      .center((-span/2) + 10, -hook_id/2 - 2.5)
      .rect(22, hook_id)
      .extrude(width)
      .center(span - 15, (hook_id/2)-(tiny_hook_id/2) + 1.0)
      .rect(8, 2)
      .extrude(width)
)

hook = hook.cut(big_cut)

# other = hook.mirror(mirrorPlane='YZ', basePointVector=(0, 0, 0))
# hook = hook.union(other)

# hook = hook.faces('<Y').edges('|Z').fillet(2.0)

cq.exporters.export(hook, 'tree.stl')