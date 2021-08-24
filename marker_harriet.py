import cadquery as cq

md_max = 23.0
holder_max_od = 75.0
holder_max_height = 80.0
wall_thickness = 5.0
inner_max = (md_max+holder_max_od)/2.0

holder = (
    cq.Workplane('XY')
      .circle(holder_max_od/2.0)
      .extrude(holder_max_height)
)

holder = (
    holder.faces(">Z")
          .workplane()
          .circle((holder_max_od-wall_thickness)/2.0)
          .cutBlind(-holder_max_height+wall_thickness)
)

marker_holder = (
    cq.Workplane('XY')
      .circle((md_max+wall_thickness)/2.0)
      .extrude(holder_max_height)
)

marker_holder = (
    marker_holder.faces(">Z")
                 .workplane()
                 .circle(md_max/2.0)
                 .cutBlind(-holder_max_height+wall_thickness)
)

inner_holder = (
    cq.Workplane('XY')
      .circle((inner_max+wall_thickness)/2.0)
      .extrude(holder_max_height)
)

inner_holder = (
    inner_holder.faces(">Z")
                 .workplane()
                 .circle(inner_max/2.0)
                 .cutBlind(-holder_max_height+wall_thickness)
)

holder = holder.union(marker_holder)
holder = holder.union(inner_holder)
holder = holder.faces(">Z").fillet(1.12)

cq.exporters.export(holder, 'harriet.stl')