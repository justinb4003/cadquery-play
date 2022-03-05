import cadquery as cq

inner_w = 18
inner_h = 31
inner_d = 20
outer_w = 25
outer_h = 38
outer_d = 2

hole_diameter = 10

plug = (
    cq.Workplane("XY")
      .rect(inner_w, inner_h)
      .extrude(inner_d)
      .faces(">Z")
      .rect(outer_w, outer_h)
      .extrude(outer_d)
)

plug = plug.edges("|Z").fillet(2)
plug = plug.faces(">Z").circle(hole_diameter/2).cutThruAll()
plug = plug.edges(">Z").chamfer(0.5)
plug = plug.edges("<Z").chamfer(1)

cq.exporters.export(plug, 'output/plug_2x1_alum.stl')