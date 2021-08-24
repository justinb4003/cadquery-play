import cadquery as cq


outer_length = 120.0
holder_max_height = 80.0

md_max = 23.0
pen_max = 12.0
wall_thickness = 5.0

outer = (
    cq.Workplane("XY")
      .polygon(3, outer_length)
      .extrude(holder_max_height)
)

outer = (
    outer.faces(">Z")
         .workplane()
         .center(20, 0)
         .circle(md_max/2.0)
         .cutBlind(-holder_max_height+wall_thickness)
)

outer = (
    outer.faces(">Z")
         .workplane()
         .center(md_max/2+wall_thickness*2, 0)
         .circle(pen_max/2.0)
         .cutBlind(-holder_max_height+wall_thickness)
)

trap = [
    (-5, 0),
    (-3, 2),
    (0, 2),
    (0, 0),
]

pens = (
    cq.Workplane("XY")
      .polyline(trap).mirrorY()
      .extrude(holder_max_height+20)
)

(L,H,W,t) = ( 100.0, 40.0, 22.0, 1.0)
pts = [
    (0,H/2.0),
    (W/2.0,H/2.0),
    (W/2.0,(H/2.0 - t)),
    (t/2.0,(H/2.0-t)),
    (t/2.0,(t - H/2.0)),
    (W/2.0,(t -H/2.0)),
    (W/2.0,H/-2.0),
    (0,H/-2.0)
]

trap_bottom = 90
trap_top = 58
trap_height= 28
pts = [
    (0, -trap_bottom/2),
    (trap_height, -trap_top/2),
    (trap_height, trap_top/2),
    (0, trap_bottom/2),
]
pens = (
    cq.Workplane("XY")
      .workplane(offset=wall_thickness)
      .center(-25, 0)
      .polyline(pts).close()
      .extrude(L)
)

holder = outer.cut(pens)
holder = holder.edges("|Z").fillet(8.0)
holder = holder.edges(">Z").fillet(1.5)

cq.exporters.export(holder, 'margaret.stl')