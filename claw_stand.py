import cadquery as cq

iw = 49
ih = 11.5
id = 20

bw = 75
bh = 40
bd = 10

insert = (
    cq.Workplane("XY")
      .rect(iw, ih)
      .extrude(id)
)

base = (
    cq.Workplane("XY")
      .workplane(invert=True)
      .rect(bw, bh)
      .extrude(bd)
)

stand = insert.union(base)
stand = stand.edges("|Z").fillet(4.0)
stand = stand.edges(">Z").fillet(2.0)

cq.exporters.export(stand, 'output/claw_stand.stl')