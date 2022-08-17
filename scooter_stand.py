import cadquery as cq

stand_h = 75

top_w = 50
top_h = 62

base_w = 120
base_h = 100
base_thick = 4

inner_base_w = base_w - 33
inner_base_h = base_h - 33

tire_slot_w = 26
tire_slot_h = inner_base_h
tire_slot_d = stand_h - 12

fork_slot_w = inner_base_w
fork_slot_h = 28
fork_slot_d = stand_h - 32

base = (
    cq.Workplane("XY")
      .rect(base_w, base_h)
      .extrude(base_thick)
)

base = base.edges("|Z").fillet(6)
base = base.faces(">Z").edges().fillet(2)

print(inner_base_w, inner_base_h, top_w, top_h)

stand = (
    base.faces(">Z")
      .rect(inner_base_w, inner_base_h)
      .workplane(offset=stand_h)
      .rect(top_w, top_h)
      .loft(combine=True)
)

tire_slot = (
    stand.faces(">Z")
         .workplane(invert=True, centerOption='CenterOfBoundBox')
         .rect(tire_slot_w, tire_slot_h)
         .extrude(tire_slot_d, combine=False)
)

fork_slot = (
    stand.faces(">Z")
         .workplane(invert=True, centerOption='CenterOfBoundBox')
         .rect(fork_slot_w, fork_slot_h)
         .extrude(fork_slot_d, combine=False)

)

stand = stand.cut(tire_slot).cut(fork_slot)

stand = stand.edges("not (<Z)").fillet(3)

stand = stand.union(base)

wheel_d = 100
wheel_w = 26

wheel = (
    cq.Workplane("YZ")
      .workplane(offset=-(wheel_w/2))
      .center(0, wheel_d/2+4)
      .circle(wheel_d/2)
      .extrude(wheel_w)
)

stand = stand.cut(wheel)

hole_offset = 22
stand = (
    stand.faces("<Z")
         .rect(base_w - hole_offset, base_h - hole_offset, forConstruction=True)
         .vertices().circle(4).cutThruAll()
)

stand = (
    stand.faces("<Z")
         .rect(base_w - hole_offset, 0, forConstruction=True)
         .vertices().circle(4).cutThruAll()
)

cq.exporters.export(stand, 'output/scooter_stand.stl')
