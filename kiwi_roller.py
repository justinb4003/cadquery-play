import cadquery as cq

base_d = 12.5
base_h = 4
inner_d = 5.7
pole_h = 9.2
pole_d = 8.7

bottom = (
    cq.Workplane("XY")
      .circle(base_d/2)
      .extrude(base_h)
      .edges(">Z").fillet(3)
)
top = (
    cq.Workplane("XY")
      .workplane(offset=pole_h+base_h)
      .circle(base_d/2)
      .extrude(base_h)
      .edges("<Z").fillet(3)
)

pole = (
    cq.Workplane("XY")
      .circle(pole_d/2)
      .extrude(pole_h + base_h*2)
)

roller = top.union(bottom).union(pole)
roller = (
    roller.faces(">Z")
    .circle(inner_d/2).cutThruAll()
)


cq.exporters.export(roller, 'output/kiwi_roller.stl')