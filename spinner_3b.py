import cadquery as cq

width = 75
height = 30
curve = 12
thickness = 7.0 
bearing_od = 22
small_bearing_od = 17.1  # slight fudge over the 606 diameter of 17mm

nut_offset = 13
nut_locations = [(-(width/2-nut_offset), 0), (width/2-nut_offset, 0)]

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
      .circle(small_bearing_od/2)
      .cutThruAll()
)

cq.exporters.export(spinner, 'output/spinner_3b.stl')
