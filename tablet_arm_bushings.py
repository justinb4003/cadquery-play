import cadquery as cq

base_od = 24
od = 15.4
id = 6 # 10-24 screw is 5mm, add a bit extra
sleeve = 12
screw_od = 12
full_depth = 27

plate_bushing = (
    cq.Workplane("XY")
      .circle(base_od / 2)
      .extrude(3)
      .faces(">Z")
      .circle(od / 2)
      .extrude(sleeve)
      .faces(">Z")
      .circle(screw_od / 2)
      .cutThruAll()
      .faces(">Z")
      .circle(od / 2)
      .extrude(full_depth-sleeve)
      .edges(">Z").chamfer(1)
      .edges("<Z").chamfer(1)
      .faces(">Z").circle(id / 2).cutThruAll()
)

cq.exporters.export(plate_bushing, 'output/plate_bushing.stl')

od = 14.0
id = 6 # 10-24 screw is 5mm, add a bit extra
height = 19
base_od = 24
base_height = 3

arm_bushing = (
    cq.Workplane("XY")
      .circle(base_od / 2) .extrude(base_height)
      .faces(">Z") .circle(od / 2) .extrude(height)
      .edges(">Z").chamfer(1)
      .faces(">Z").circle(id / 2).cutThruAll()
      .edges("<Z").chamfer(1)
)


"""
nut_hole = (
    arm_bushing.faces(">Z")
        .workplane(invert=True)
        .polygon(6, 11)
        .extrude(7, combine=False)
)

arm_bushing = arm_bushing.cut(nut_hole)
"""

cq.exporters.export(arm_bushing, 'output/arm_bushing.stl')