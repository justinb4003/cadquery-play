import cadquery as cq


pixy2 = cq.importers.importStep('pixy2.step')

screw_hole_height = 16


case = (
    cq.Workplane("XY")
      .center(-3.2, -21.3)
      .circle(3/2).extrude(-screw_hole_height)
      .center(6.4, 0)
      .circle(3/2).extrude(-screw_hole_height)
      .center(-(22.4-5.1), (38.8-31.3))
      .circle(3/2).extrude(-screw_hole_height)
)

wall_thickness = 5
plate = (
    cq.Workplane("XY")
      .workplane(offset=-10)
      .rect(38.25+wall_thickness, 42+wall_thickness)
      .extrude(-6)
)

header_cut = (
    cq.Workplane("XY")
      .workplane(offset=-10)
      .center(-13, 3)
      .rect(9, 29)
      .extrude(-6, combine=False)
)

plate = plate.cut(header_cut)

cq.exporters.export(case, 'output/pixy2_case.stl')
cq.exporters.export(plate, 'output/pixy2_plate.stl')

