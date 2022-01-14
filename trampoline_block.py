import cadquery as cq

inch = 25.4

block = (
    cq.Workplane("XY")
      .rect(40, 30)
      .extrude(25)
      .faces(">Y").workplane(centerOption="CenterOfBoundBox")
      .circle(13/2).cutThruAll()
      .faces(">Z").workplane(centerOption="CenterOfBoundBox")
      .center(0, 16)
      .circle(16).cutThruAll()
      .center(0, -(16+6+39/2))
      .circle(39/2).cutThruAll()
)

cq.exporters.export(block, 'output/trampoline_block.stl')