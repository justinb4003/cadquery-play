import cadquery as cq

bottle1_od = 50.0
bottle2_od = 38.0
rack_height = 40
funnel_depth = 8
bottle_padding = 15
bottles = 2

lid_inner_height = 110
lid_thickness = 2.5

avg_bottle_od = (bottle1_od+bottle2_od)/2

block_width = bottles * (avg_bottle_od + bottle_padding) + 15
block_depth = (bottle1_od + bottle_padding) + 10

def cut_hole(body, x, y, bottle_od):
    funnel_od = bottle_od + 5
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

rack = (
    cq.Workplane("XY")
      .rect(block_width, block_depth)
      .extrude(rack_height)
)


rack = cut_hole(rack, 32, 0, bottle1_od)
rack = cut_hole(rack, -36, 0, bottle2_od)
# rack = cut_hole(rack, (funnel_od+bottle_padding/2), 0)

rack = rack.edges("|Z").fillet(12.0)
rack = rack.edges(">Z").fillet(1.0)

lid =  (
    cq.Workplane("XY")
      .rect(block_width + lid_thickness*2, block_depth + lid_thickness*2)
      .extrude(lid_inner_height+lid_thickness)
)

lid = lid.edges("|Z").fillet(12.0)

lid_cut = (
    cq.Workplane("XY")
      .rect(block_width+0.1, block_depth+0.1)
      .extrude(lid_inner_height)
      .edges("|Z").fillet(12)

)

lid = lid.cut(lid_cut)


cq.exporters.export(rack, 'output/backpain.stl')
cq.exporters.export(lid, 'output/backpain_lid.stl')
