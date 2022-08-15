import cadquery as cq

lid_fudge = 1.2
lid_thick = 4
box_d = 26 + lid_fudge
box_l = 63 + lid_fudge
lid_d = box_d + lid_thick * 2
lid_l = box_l + lid_thick * 2

lid_top_h = 39
lid_total_h = 64


lid = (
    cq.Workplane("XY")
      .rect(lid_d, lid_l)
      .extrude(lid_total_h + lid_thick)
)

box_cut = (
    cq.Workplane("XY")
      .rect(box_d, box_l)
      .extrude(lid_total_h)
)

lid = lid.cut(box_cut)

tokencut = (
    lid.faces("<Z")
        .workplane(invert=True, centerOption='CenterOfBoundBox')
        .center(0, -lid_thick)
        .rect(lid_d, lid_l)
        .extrude(20, combine=False)
)

lid = lid.cut(tokencut)

lid = (
    lid
    .edges("|Y").fillet(1)
    .edges("|Z and <Y").fillet(1)
    .edges("|Z and >Y").fillet(1)
)

diamond_cut = (
    lid.faces(">Y")
        .workplane(invert=True, centerOption='CenterOfBoundBox')
        .center(0, 13.5)
        .circle(6)
        .extrude(lid_thick, combine=False)
)

lid = lid.cut(diamond_cut)


cq.exporters.export(lid, 'output/mayhem_lid_thicker.stl')