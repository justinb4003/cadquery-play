import cadquery as cq

wall_offset = 10
dowel_d = 29.5
bracket_width = 200
bracket_height = 160
bracket_thickness = 25
dowel_inset = dowel_d/2 + 4
bracket = (
    cq.Workplane("XY")
      .lineTo(bracket_width, 0)
      .lineTo(0, -bracket_height)
      .close()
      .extrude(bracket_thickness)
)

for n in range(4):
    dowel_hole = (
        cq.Workplane("XY")
        .moveTo(wall_offset + dowel_d/2 + (n*40), -dowel_inset)
        .circle(dowel_d/2)
        .extrude(bracket_thickness, combine=False)
    )
    bracket = bracket.cut(dowel_hole)

cutoffset = -40
cutinset = 15
scale = 0.6
bigcut = (
    cq.Workplane("XY")
      .moveTo(cutinset, cutoffset)
      .lineTo(bracket_width * scale, cutoffset)
      .lineTo(cutinset, -bracket_height*0.8)
      .lineTo(cutinset, cutoffset)
      .close()
      .extrude(bracket_thickness + 25)
)

bracket = bracket.cut(bigcut)

bracket = bracket.edges("|Z").fillet(10)

# build holes for deck screws
screw_hole_d = 5.5
top_x = 50
bottom_x = -15 
bracket = (
    bracket.faces("-X")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(top_x, 0).circle(screw_hole_d/2).cutThruAll()
    .moveTo(bottom_x, 0).circle(screw_hole_d/2).cutThruAll()
)

# build around a half inch (12mm) hole for a washer around said screw
screw_hole_d = 12 
top_x = 50
bottom_x = -15 
washer_holes = (
    bracket.faces("-X")
    .workplane(offset=5, invert=True, centerOption="CenterOfBoundBox")
    .moveTo(top_x, 0).circle(screw_hole_d/2).extrude(90, combine=False)
    .moveTo(bottom_x, 0).circle(screw_hole_d/2).extrude(50, combine=True)
)

bracket = bracket.cut(washer_holes)

cq.exporters.export(bracket, 'output/filament_dowel_bracket.stl')

# show_object(bracket)
