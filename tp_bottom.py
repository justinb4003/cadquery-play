import cadquery as cq

plate = (
    cq.Workplane("XY")
      .circle(140)
      .extrude(5)
      .faces(">Z")
      .workplane()
      .circle(56)
      .extrude(6)
      .faces(">Z")
      .workplane()
      .circle(15)
      .cutThruAll()
)

cq.exporters.export(plate, 'output/tp_bottom.stl')