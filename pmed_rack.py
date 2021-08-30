import cadquery as cq

bottle_od = 33.0
rack_height = 40
funnel_depth = 8
funnel_od = 38.0
bottle_padding = 10

bottles = 3
block_width = bottles * (bottle_od + bottle_padding)
block_depth = (bottle_od + bottle_padding)

rack = (
    cq.Workplane("XY")
      .rect(block_width, block_depth)
      .extrude(rack_height)
)

def cut_hole(body, x, y):
    hole = (
        body.faces(">Z")
            .workplane(invert=True)
            .center(x, y)
            .circle(funnel_od / 2.0)
            .workplane(offset=funnel_depth)
            .circle(bottle_od/2.0)
            .loft(combine=False)
    )
    body = body.cut(hole)
    hole = (
        body.faces(">Z")
            .workplane(invert=True)
            .center(x, y)
            .circle(bottle_od / 2.0)
            .extrude(rack_height-3, combine=False)
    )
    body = body.cut(hole)
    hole = (
        body.faces(">Z")
            .workplane(invert=True)
            .center(x, y)
            .circle((bottle_od-10) / 2.0)
            .extrude(rack_height, combine=False)
    )
    body = body.cut(hole)
    return body

rack = cut_hole(rack, 0, 0)
rack = cut_hole(rack, -(funnel_od+bottle_padding/2), 0)
rack = cut_hole(rack, (funnel_od+bottle_padding/2), 0)

rack = rack.edges("|Z").fillet(12.0)
rack = rack.edges(">Z").fillet(1.0)


cq.exporters.export(rack, 'output/medrack.stl')
