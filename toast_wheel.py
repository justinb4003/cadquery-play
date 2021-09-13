import cadquery as cq

inch = 25.4

wheel_width = 0.25 * inch
wheel_diameter = 6 * inch

pattern_length = 1.875 * inch / 2

wheel = (
    cq.Workplane("XY")
      .circle(wheel_diameter / 2)
      .extrude(wheel_width)
)

wheel = (
    wheel.faces(">Z")
        .workplane()
        .circle(1.25*inch/2)
        .cutThruAll()
)
wheel = (
    wheel.faces(">Z")
        .workplane()
        .polygon(6, 1.875*inch, forConstruction=True)
        .vertices()
        .circle((3/16)*inch/2)
        .cutThruAll()
)

cq.exporters.export(wheel, 'output/toast_wheel.stl')