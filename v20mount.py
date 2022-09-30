import cadquery as cq

base_l = 58
base_w = 66
base_d = 10

holder = (
    cq.Workplane("XY")
      .rect(base_l, base_w)
      .extrude(base_d)
)

post_l = base_l
post_w = 41
post_d = 7


holder = (
    holder.faces(">Z")
    .rect(post_l, post_w)
    .extrude(post_d)
)

lip_l = base_l
lip_w = 53
lip_extension = 14
lip_offset = 5
lip = (
    holder.faces(">Z")
    .workplane()
    .center(lip_l/2 - lip_extension, lip_w/2) # Top right corner
    .line(lip_extension, -lip_offset)
    .line(0, -(lip_w-(lip_offset*2)))
    .line(-lip_extension, -lip_offset)
    .line(-(lip_l-lip_extension), 0)
    .line(0, lip_w).close().extrude(5.2, combine=False)
)

lip = lip.edges("not (<X or >X)").fillet(2)

holder = holder.union(lip)

holder = (
holder.faces(">Z")
.rect(base_l / 1.8, 0, forConstruction=True).vertices().cboreHole(5, 10, 3)
# .rect(base_l / 1.8, 0, forConstruction=True).vertices().circle(2).cutThruAll()
)


cq.exporters.export(holder, 'output/v20mount.stl')