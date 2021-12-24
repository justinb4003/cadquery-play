import cadquery as cq

width = 75
height = 35
curve = 10
thickness = 7
bearing_od = 22

nut_offset = 13
nut_locations = [(-(width/2-nut_offset), 0), (width/2-nut_offset, 0)]
nut_diameter = 14.05

spinner = (
    cq.Workplane("XY")
      .rect(width, height)
      .extrude(thickness)
      .edges("|Z").fillet(curve)
      .edges("|X").chamfer(2)
      .circle(bearing_od/2)
      .cutThruAll()
      .faces(">Z")
      .pushPoints(nut_locations)
      .polygon(6, nut_diameter).cutThruAll()
)

cq.exporters.export(spinner, 'output/spinner.stl')