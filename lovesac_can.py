import cadquery as cq

insert_od = 88
can_od = 68
insert_h = 50

insert = (
    cq.Workplane("XY")
      .circle(insert_od/2)
      .extrude(insert_h)
)

bottom_thickness = 3
cancut = (
    cq.Workplane("XY")
    .workplane(offset=bottom_thickness,
               centerOption='CenterOfMass')
    .circle(can_od/2)
    .extrude(insert_h+bottom_thickness-15, combine=False)
)

cancut = (
    cancut.faces(">Z")
    .circle(can_od/2)
    .workplane(offset=15)
    .circle((insert_od-10)/2)
    .loft(combine=True)
)

insert = insert.cut(cancut)
insert = insert.edges(">Z").fillet(3)
insert = insert.edges("<Z").chamfer(3)
insert = insert.faces("<Z").circle(12).cutThruAll()

cq.exporters.export(insert, 'output/lovesac_can.stl')
