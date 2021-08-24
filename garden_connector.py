import cadquery as cq

thickness = 3.0
length = 40.0
free_fall = (length/2)-5
max_id = 16.5
min_id = 12

body = (
    cq.Workplane("XY")
      .circle((max_id+thickness)/2)
      .extrude(length)
)

tophole = (
    body.faces(">Z")
        .workplane()
        .circle(max_id/2)
        .workplane(offset=free_fall, invert=True)
        .circle(max_id/2)
        .workplane(offset=5)
        .circle(min_id/2)
        .loft(combine=False)
)

bottomhole = (
    body.faces("<Z")
        .workplane()
        .circle(max_id/2)
        .workplane(offset=free_fall, invert=True)
        .circle(max_id/2)
        .workplane(offset=5)
        .circle(min_id/2)
        .loft(combine=False)
)

s = cq.selectors.StringSyntaxSelector

body = body.edges(s(">Z") + s("<Z")).fillet(1)

body = body.cut(tophole)
body = body.cut(bottomhole)


cq.exporters.export(body, 'garden.stl')