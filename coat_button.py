import cadquery as cq

button_od = 25
dip_od = 20
dip_height = 2
button_height = 4
hole_d = 2
hole_spacing = 6

button = (
    cq.Workplane("XY")
        .circle(button_od/2)
        .extrude(button_height)
)

button_cut = (
    button.faces(">Z")
        .workplane(invert=True, centerOption='CenterOfMass')
        .circle(dip_od/2)
        .extrude(dip_height, combine=False)
)

button = button.cut(button_cut)

button = (
    button.faces("<Z")
        .rect(hole_spacing, hole_spacing, forConstruction=True)
        .vertices()
        .circle(hole_d/2)
        .cutThruAll()
)


cq.exporters.export(button, 'output/coat_button.stl')