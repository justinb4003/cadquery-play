import cadquery as cq

top_hanger_id = 12.5
bottom_hanger_id = 30.0
thickness = 4.0
width = 14
drop_height = 15

def make_half_circle(r):
  hc = (
    cq.Workplane("XY")
      .lineTo(-r, 0)
      .threePointArc((0, r), (r, 0))
      .close()
  )
  return hc


top_cut = make_half_circle(top_hanger_id/2).extrude(width)
top_hanger = make_half_circle(top_hanger_id/2+(thickness)).extrude(width)
hook = top_hanger.cut(top_cut)
hook = (
  hook.faces("<Y")
  .workplane(centerOption="CenterOfMass")
  .circle(1)
  .extrude(10)
)
"""
hook = hook.edges("|Z").fillet(1.5)
hook = hook.cut(hanger_cut)
hook = hook.faces(">X").edges(">Y").fillet(3)
"""

cq.exporters.export(hook, 'output/light_hook.stl')