import cadquery as cq

inch = 25.4

wheel_width = 0.75 * inch
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
        .cboreHole((3/16)*inch, (3/8)*inch, (1/4)*inch)
)

wheel = (
    wheel.faces(">Z")
        .workplane(invert=True)
        .polygon(30, wheel_diameter, forConstruction=True)
        .vertices()
        .polygon(6, 8)
        .extrude(wheel_width)
)

cq.exporters.export(wheel, 'output/toast_wheel.stl')