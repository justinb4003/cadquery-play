import cadquery as cq

od = 14
handle_height = 72.0
shaft_width = 8.05

tube = (
    cq.Workplane("XY")
      .circle(od/2)
      .extrude(handle_height)
)

shaft = (
    tube.faces(">Z")
        .rect(shaft_width, shaft_width)
        .extrude(-12, combine=False)
)

tee = (
    cq.Workplane("XZ")
      .workplane(offset=-2.0)
      .center(0, 12.5)
      .rect(60, 25)
      .extrude(4)
)

tube = tube.cut(shaft)
tube = tube.edges(">Z").chamfer(0.5)
tube = tube.union(tee)

cq.exporters.export(tube, 'output/gaskey.stl')