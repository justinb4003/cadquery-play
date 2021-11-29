import cadquery as cq

remote_depth = 9
remote_width = 51
pocket_height = 20
total_height = 60
shell_thickness = 3.0

shell = (
    cq.Workplane("XY")
      .rect(51+shell_thickness*2, 9+shell_thickness*2)
      .extrude(pocket_height)
)

holder = (
    cq.Workplane("XY")
      .workplane(offset=shell_thickness)
      .rect(51, 9)
      .extrude(pocket_height)
)

backing = (
    cq.Workplane("XY")
      .center(0, (remote_depth+shell_thickness)/2)
      .rect(51+shell_thickness*2, shell_thickness*2)
      .extrude(total_height)
)

holder = shell.cut(holder)
holder = holder.edges("|Z").fillet(4.0)
holder = holder.edges("|X").fillet(1.0)
backing = backing.edges("|Z").fillet(1.0)
backing = backing.edges("|X").fillet(1.0)
holder = holder.union(backing)

cq.exporters.export(holder, 'output/heater_remote.stl')
