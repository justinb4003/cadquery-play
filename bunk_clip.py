import cadquery as cq

hook_id = 28
span = 120
thickness = 12
width = 20


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
        .center(span, 0)
        .circle((hook_id+thickness) / 2.0)
        .extrude(width)
)

hook = bar.union(hook)


holes = (
    cq.Workplane("XY")
        .center(-span/2, -hook_id/2 - 0)
        .circle((hook_id) / 2.0)
        .extrude(width+20)
        .center(span, 0)
        .circle((hook_id) / 2.0)
        .extrude(width)
)

hook = hook.cut(holes)

big_cut = (
    cq.Workplane("XY")
      .center(0, -(hook_id+thickness)/2)
      .rect(span-5, (hook_id+thickness)) 
      .extrude(width)
)

hook = hook.cut(big_cut)
# other = hook.mirror(mirrorPlane='YZ', basePointVector=(0, 0, 0))
# hook = hook.union(other)

hook = hook.faces('<Y').edges('|Z').fillet(2.0)

cq.exporters.export(hook, 'hook.stl')