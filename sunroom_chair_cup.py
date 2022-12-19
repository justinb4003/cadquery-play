import cadquery as cq

cup_h_id = 90
cup_h_thick = 6
cup_h_height = 50

cup_holder = (
    cq.Workplane("XY")
      .circle(cup_h_id/2+cup_h_thick)
      .extrude(cup_h_height+cup_h_thick)
)

cup_cut = (
    cup_holder.faces(">Z")
        .workplane(invert=True, centerOption='CenterOfMass')
        .circle(cup_h_id/2)
        .extrude(cup_h_height, combine=False)
)

cup_holder = cup_holder.cut(cup_cut)

cup_holder = cup_holder.faces("<Z").edges().fillet(4)

cup_holder = (
    cup_holder.faces(">Z[-2]")
    .cboreHole(3.5, 6.5, 3)
)
cup_holder = cup_holder.faces(">Z").edges().fillet(2)

clip_width = 50
arm_width = 37
thickness = 5
depth = 50
outline = [
    (0, 0),
    (arm_width+thickness*2, 0),
    (arm_width+thickness*2, depth+thickness),
    (arm_width+thickness*1, depth+thickness),
    (arm_width+thickness*1, thickness),
    (thickness, thickness),
    (thickness, depth+thickness),
    (0, depth+thickness)
]

clip = (
    cq.Workplane("XY")
        .polyline(outline).close()
        .extrude(clip_width)
).edges(">Y and |Z").fillet(thickness/4)

# Make room for threaded nut insert
clip = (
    clip.faces("<Y")
        .workplane(centerOption='CenterOfMass')
        .circle(2).cutThruAll()
)



cq.exporters.export(cup_holder, 'output/sunroom_cup_holder_top.stl')
cq.exporters.export(clip, 'output/sunroom_cup_holder_clip.stl')